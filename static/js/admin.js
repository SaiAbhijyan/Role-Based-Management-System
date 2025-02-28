document.addEventListener("DOMContentLoaded", function() {
    console.log("Admin Dashboard Loaded");
});

// Load a section based on selection (employees, users, or roles)
function loadSection(section) {
    let contentArea = document.getElementById("contentArea");

    if (section === "employees") {
        fetchEmployees();
    } else if (section === "users") {
        fetchUsers();
    } else if (section === "roles") {
        fetchRoles_table();
    }
}

// Fetch employees and display them in a table (unchanged)
function fetchEmployees() {
    fetch('/admin/employees')
        .then(response => response.json())
        .then(data => {
            let contentArea = document.getElementById("contentArea");
            let tableHtml = `
                <h3>Employee Records</h3>
                <table border="1" class="w3-table-all">
                    <thead>
                        <tr>
                            <th>E_ID</th>
                            <th>Name</th>
                            <th>Designation</th>
                            <th>Salary</th>
                            <th>Bonus</th>
                            <th>State</th>
                            <th>Zip Code</th>
                            <th>Department</th>
                        </tr>
                    </thead>
                    <tbody>`;

            data.forEach(emp => {
                tableHtml += `
                    <tr>
                        <td>${emp.E_id}</td>
                        <td>${emp.E_name}</td>
                        <td>${emp.Designation}</td>
                        <td>$${emp.Salary}</td>
                        <td>$${emp.Bonus}</td>
                        <td>${emp.State}</td>
                        <td>${emp.Zip_Code}</td>
                        <td>${emp.Department}</td>
                    </tr>`;
            });

            tableHtml += `</tbody></table>`;
            contentArea.innerHTML = tableHtml;
        })
        .catch(error => console.error("Error fetching employees:", error));
}

// Global variable to store roles data
let rolesData = [];

// Fetch dynamic role options from the server
function fetchRoles() {
    return fetch('/admin/roles_dropdown')
        .then(response => response.json())
        .then(data => {
            rolesData = data; // store roles globally
            return data;
        })
        .catch(error => {
            console.error("Error fetching roles:", error);
        });
}

// Populate the role dropdown for each user row
function populateRoleDropdowns() {
    // First, fetch roles if not already loaded
    if (rolesData.length === 0) {
        fetchRoles().then(() => {
            populateDropdowns();
        });
    } else {
        populateDropdowns();
    }

    function populateDropdowns() {
        // For each user row, find the select element by id and populate options
        document.querySelectorAll("select[id^='roleSelect-']").forEach(selectElem => {
            // Clear any existing options
            selectElem.innerHTML = "";
            rolesData.forEach(role => {
                let option = document.createElement("option");
                option.value = role.role_id;
                option.text = `${role.role_id} - ${role.role_name}`;
                selectElem.appendChild(option);
            });
        });
    }
}

// Fetch users and display them in a table with a dropdown and assign button for role update
function fetchUsers() {
    fetch('/admin/users')
        .then(response => response.json())
        .then(data => {
            let contentArea = document.getElementById("contentArea");
            let tableHtml = `
                <h3>User Records</h3>
                <table border="1" class="w3-table-all">
                    <thead>
                        <tr>
                            <th>Employee ID</th>
                            <th>Employee Name</th>
                            <th>User ID</th>
                            <th>Username</th>
                            <th>Role Name</th>
                            <th>Role ID</th>
                            <th>Update Role Id</th>
                            <th>Notification</th>
                        </tr>
                    </thead>
                    <tbody>`;

            data.forEach(user => {
                tableHtml += `
                    <tr>
                        <td>${user.Employee_id !== null ? user.Employee_id : 'N/A'}</td>
                        <td>${user.Employee_name !== null ? user.Employee_name : 'N/A'}</td>
                        <td>${user.user_id}</td>
                        <td>${user.user_name}</td>
                        <td>${user.Role_name}</td>
                        <td>${user.role_id}</td>
                        <td>
                            <select id="roleSelect-${user.Employee_id}"></select>
                            <button onclick="assignRole(${user.Employee_id})">Assign</button>
                        </td>
                        <td id="updateMsg-${user.Employee_id}"></td>
                    </tr>`;
            });

            tableHtml += `</tbody></table>`;
            contentArea.innerHTML = tableHtml;
            // Populate the dropdowns for all rows
            populateRoleDropdowns();
        })
        .catch(error => console.error("Error fetching users:", error));
}

// Function to assign a new role to a user
function assignRole(employeeId) {
    let selectElem = document.getElementById(`roleSelect-${employeeId}`);
    let selectedRoleId = selectElem.value;
    let msgSpan = document.getElementById(`updateMsg-${employeeId}`);
    
    // Clear any previous message
    msgSpan.textContent = "";

    fetch('/admin/update_role', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            employee_id: employeeId,
            role_id: selectedRoleId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            msgSpan.style.color = "green";
            msgSpan.textContent = data.success;
            // Optionally, refresh the users list if needed:
            // fetchUsers();
        } else if (data.error) {
            msgSpan.style.color = "red";
            msgSpan.textContent = data.error;
        }
    })
    .catch(error => {
        console.error("Error updating role:", error);
        msgSpan.style.color = "red";
        msgSpan.textContent = "Error updating role.";
    });
}

function fetchRoles_table()
    {
        fetch('/admin/roles')
        .then(response => response.json())
        .then(data => 
        {
            let contentArea = document.getElementById("contentArea");
            let tableHtml = `
                <h3>Roles table</h3>
                <table border="1" class="w3-table-all">
                    <thead>
                        <tr>
                            <th>Role_ID</th>
                            <th>Role_Name</th>
                        </tr>
                    </thead>
                    <tbody>`;

            data.forEach(role => {
                tableHtml += `
                    <tr>
                        <td>${role.Role_ID}</td>
                        <td>${role.Role_Name}</td>
                    </tr>`;
            });

            tableHtml += `</tbody></table>`;
            contentArea.innerHTML = tableHtml;

        } 
        )
    }