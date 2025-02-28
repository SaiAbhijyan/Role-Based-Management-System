
document.addEventListener("DOMContentLoaded", function() {
    loadFilters();
    fetchEmployees();
});

function loadFilters() {
    fetch('/manager/get_filters')
        .then(response => response.json())
        .then(data => {
            let departmentDropdown = document.getElementById("department");
            let stateDropdown = document.getElementById("state");

            // Reset dropdowns and populate them with real values
            departmentDropdown.innerHTML = `<option value="">All Departments</option>`;
            stateDropdown.innerHTML = `<option value="">All States</option>`;

            // Populate Department Dropdown
            data.departments.forEach(dep => {
                let option = document.createElement("option");
                option.value = dep;
                option.textContent = dep;
                departmentDropdown.appendChild(option);
            });

            // Populate State Dropdown
            data.states.forEach(state => {
                let option = document.createElement("option");
                option.value = state;
                option.textContent = state;
                stateDropdown.appendChild(option);
            });
        })
        .catch(error => console.error("Error loading filters:", error));
}

function fetchEmployees() {
    let department = document.getElementById("department").value;
    let state = document.getElementById("state").value;
    let search_name = document.getElementById("search_name").value;

    fetch(`/manager/employees?department=${department}&state=${state}&search_name=${search_name}`)
        .then(response => response.json())
        .then(data => {
            let tableBody = document.getElementById("employeeTable").querySelector("tbody");
            tableBody.innerHTML = "";

            if (!data.length) {
                tableBody.innerHTML = "<tr><td colspan='5'>No employees found</td></tr>";
                return;
            }

            data.forEach(emp => {
                let row = `<tr>
                    <td>${emp.E_id}</td>
                    <td>${emp.E_name}</td>
                    <td>${emp.Designation}</td>
                    <td>${emp.Department}</td>
                    <td>${emp.Department_ID}</td>
                </tr>`;
                tableBody.innerHTML += row;
            });
        })
        .catch(error => console.error("Error fetching employees:", error));
}

function resetFilters() {
    document.getElementById("department").value = "";
    document.getElementById("state").value = "";
    document.getElementById("search_name").value = "";
    fetchEmployees();
}

function sortTable(columnIndex) {
    let table = document.getElementById("employeeTable");
    let rows = Array.from(table.rows).slice(1);
    let ascending = table.dataset.sortOrder !== "asc";

    rows.sort((a, b) => {
        let valA = a.cells[columnIndex].innerText;
        let valB = b.cells[columnIndex].innerText;

        return ascending ? valA.localeCompare(valB) : valB.localeCompare(valA);
    });

    rows.forEach(row => table.appendChild(row));
    table.dataset.sortOrder = ascending ? "asc" : "desc";
}
