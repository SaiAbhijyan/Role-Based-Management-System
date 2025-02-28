document.addEventListener("DOMContentLoaded", function() {
    console.log("HR Dashboard Loaded");
});

// Fetch and display all employees
function fetchEmployees() {
    fetch('/HR/employees')
        .then(response => response.json())
        .then(data => {
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
            document.getElementById("contentArea").innerHTML = tableHtml;
        })
        .catch(error => console.error("Error fetching employees:", error));
}

// Show Add Employee form
function showAddEmployeeForm() {
    let formHtml = `
        <h3>Add New Employee</h3>
        <form id="addEmployeeForm">
            <label for="empName">Employee Name:</label><br>
            <input type="text" id="empName" name="empName" required><br><br>
            
            <label for="designation">Designation:</label><br>
            <input type="text" id="designation" name="designation" required><br><br>
            
            <label for="salary">Salary:</label><br>
            <input type="number" id="salary" name="salary" step="0.01" required><br><br>
            
            <label for="bonus">Bonus:</label><br>
            <input type="number" id="bonus" name="bonus" step="0.01" required><br><br>
            
            <label for="state">State:</label><br>
            <input type="text" id="state" name="state" required><br><br>
            
            <label for="zipCode">Zip Code:</label><br>
            <input type="text" id="zipCode" name="zipCode" required><br><br>
            
            <label for="depId">Department ID:</label><br>
            <select id="depId" name="depId" required>
                <option value="">--Select Department--</option>
            </select><br><br>
            
            <button type="button" onclick="addEmployee()">Submit</button>
        </form>
        <div id="formMsg" style="margin-top:10px;"></div>
    `;
    document.getElementById("contentArea").innerHTML = formHtml;
    fetchDepartments();  // Populate department dropdown
}

// Fetch departments for Add Employee form
function fetchDepartments() {
    fetch('/HR/departments')
        .then(response => response.json())
        .then(data => {
            let depSelect = document.getElementById("depId");
            data.forEach(dep => {
                let option = document.createElement("option");
                option.value = dep.dep_id;
                option.text = dep.dep_id;
                depSelect.appendChild(option);
            });
        })
        .catch(error => console.error("Error fetching departments:", error));
}

// Add a new employee via AJAX
function addEmployee() {
    let empName = document.getElementById("empName").value.trim();
    let designation = document.getElementById("designation").value.trim();
    let salary = document.getElementById("salary").value;
    let bonus = document.getElementById("bonus").value;
    let state = document.getElementById("state").value.trim();
    let zipCode = document.getElementById("zipCode").value.trim();
    let depId = document.getElementById("depId").value;
    let formMsg = document.getElementById("formMsg");

    // Client-side validations
    if (!empName) {
        formMsg.style.color = "red";
        formMsg.textContent = "Employee Name cannot be empty.";
        return;
    }
    if (!designation) {
        formMsg.style.color = "red";
        formMsg.textContent = "Designation cannot be empty.";
        return;
    }
    if (!/^\d{5}$/.test(zipCode)) {
        formMsg.style.color = "red";
        formMsg.textContent = "Zip Code must be exactly 5 digits.";
        return;
    }

    let payload = {
        employee_name: empName,
        designation: designation,
        salary: salary,
        bonus: bonus,
        state: state,
        zip_code: zipCode,
        dep_id: depId
    };

    fetch('/HR/add_employee', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        let msgElem = document.getElementById("formMsg");
        if (data.success) {
            msgElem.style.color = "green";
            msgElem.textContent = data.success;
            document.getElementById("addEmployeeForm").reset();
        } else if (data.error) {
            msgElem.style.color = "red";
            msgElem.textContent = data.error;
        }
    })
    .catch(error => {
        console.error("Error adding employee:", error);
        let msgElem = document.getElementById("formMsg");
        msgElem.style.color = "red";
        msgElem.textContent = "Error adding employee.";
    });
}

// Show Update Employee Filter Form
function showUpdateEmployeeFilterForm() {
    let filterHtml = `
        <h3>Filter Employees for Update</h3>
        <form id="filterForm">
            <label for="filterName">Employee Name:</label><br>
            <input type="text" id="filterName" name="filterName" placeholder="Partial name"><br><br>
            
            <label for="filterState">State:</label><br>
            <select id="filterState" name="filterState">
                <option value="">--Select State--</option>
            </select><br><br>
            
            <label for="filterDep">Department:</label><br>
            <select id="filterDep" name="filterDep">
                <option value="">--Select Department--</option>
            </select><br><br>
            
            <button type="button" onclick="applyEmployeeFilter()">Apply Filter</button>
        </form>
        <div id="filterMsg" style="margin-top:10px;"></div>
        <div id="filterResults"></div>
    `;
    document.getElementById("contentArea").innerHTML = filterHtml;
    fetchFilterStates();
    fetchFilterDepartments();
}

// Fetch states for filter form (from payroll.tax_deductions)
function fetchFilterStates() {
    fetch('/HR/filter_states')
        .then(response => response.json())
        .then(data => {
            let stateSelect = document.getElementById("filterState");
            data.forEach(item => {
                let option = document.createElement("option");
                option.value = item.state;
                option.text = item.state;
                stateSelect.appendChild(option);
            });
        })
        .catch(error => console.error("Error fetching filter states:", error));
}

// Fetch departments for filter form (reuse /HR/departments)
function fetchFilterDepartments() {
    fetch('/HR/departments')
        .then(response => response.json())
        .then(data => {
            let depSelect = document.getElementById("filterDep");
            data.forEach(dep => {
                let option = document.createElement("option");
                option.value = dep.dep_id;
                option.text = dep.dep_id;
                depSelect.appendChild(option);
            });
        })
        .catch(error => console.error("Error fetching filter departments:", error));
}

// Apply filter and fetch filtered employees
function applyEmployeeFilter() {
    let filterName = document.getElementById("filterName").value.trim();
    let filterState = document.getElementById("filterState").value;
    let filterDep = document.getElementById("filterDep").value;
    
    let payload = {
        employee_name: filterName,
        state: filterState,
        dep_id: filterDep
    };

    fetch('/HR/filter_employees', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        let resultsDiv = document.getElementById("filterResults");
        if (data.error) {
            resultsDiv.innerHTML = `<p style="color:red;">${data.error}</p>`;
        } else {
            let tableHtml = `
                <h3>Filtered Employees</h3>
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
                            <th>Update</th>
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
                        <td><button onclick='openUpdateModal(${JSON.stringify(emp)})'>Update</button></td>
                    </tr>`;
            });
            tableHtml += `</tbody></table>`;
            resultsDiv.innerHTML = tableHtml;
        }
    })
    .catch(error => console.error("Error applying filter:", error));
}

// Open update modal with pre-populated data from the employee record
function openUpdateModal(employee) {
    let modal = document.getElementById("updateModal");
    let modalContent = document.getElementById("updateModalContent");
    
    let formHtml = `
        <h3>Update Employee</h3>
        <form id="updateEmployeeForm">
            <input type="hidden" id="updEId" value="${employee.E_id}">
            <label for="updEmpName">Employee Name:</label><br>
            <input type="text" id="updEmpName" value="${employee.E_name}"><br><br>
            
            <label for="updDesignation">Designation:</label><br>
            <input type="text" id="updDesignation" value="${employee.Designation}"><br><br>
            
            <label for="updSalary">Salary:</label><br>
            <input type="number" id="updSalary" value="${employee.Salary}" step="0.01"><br><br>
            
            <label for="updBonus">Bonus:</label><br>
            <input type="number" id="updBonus" value="${employee.Bonus}" step="0.01"><br><br>
            
            <label for="updState">State:</label><br>
            <input type="text" id="updState" value="${employee.State}"><br><br>
            
            <label for="updZipCode">Zip Code:</label><br>
            <input type="text" id="updZipCode" value="${employee.Zip_Code}"><br><br>
            
            <label for="updDepId">Department:</label><br>
            <select id="updDepId"></select><br><br>
            
            <button type="button" onclick="updateEmployee()">Submit</button>
        </form>
    `;
    modalContent.innerHTML = formHtml;
    modal.style.display = "block";
    // Populate department dropdown in update modal
    fetch('/HR/departments')
        .then(response => response.json())
        .then(data => {
            let depSelect = document.getElementById("updDepId");
            depSelect.innerHTML = "";
            data.forEach(dep => {
                let option = document.createElement("option");
                option.value = dep.dep_id;
                option.text = dep.dep_id;
                if (dep.dep_id == employee.Department || dep.dep_id == employee.dep_id) {
                    option.selected = true;
                }
                depSelect.appendChild(option);
            });
        })
        .catch(error => console.error("Error fetching departments for update:", error));
    
    // Store original values for client-side comparison
    document.getElementById("updateEmployeeForm").dataset.original = JSON.stringify({
        employee_name: employee.E_name,
        designation: employee.Designation,
        salary: employee.Salary,
        bonus: employee.Bonus,
        state: employee.State,
        zip_code: employee.Zip_Code,
        dep_id: employee.Department
    });
    // Clear any previous update message
    document.getElementById("updateMsg").textContent = "";
}

// Close the update modal
function closeUpdateModal() {
    document.getElementById("updateModal").style.display = "none";
}

// Update employee via AJAX with client-side check
function updateEmployee() {
    let form = document.getElementById("updateEmployeeForm");
    let originalData = JSON.parse(form.dataset.original);
    
    let employeeId = document.getElementById("updEId").value;
    let newData = {
        employee_name: document.getElementById("updEmpName").value.trim(),
        designation: document.getElementById("updDesignation").value.trim(),
        salary: document.getElementById("updSalary").value,
        bonus: document.getElementById("updBonus").value,
        state: document.getElementById("updState").value.trim(),
        zip_code: document.getElementById("updZipCode").value.trim(),
        dep_id: document.getElementById("updDepId").value
    };
    
    // Client-side check: if no field has changed or a field is empty, skip updating that field
    let changedData = {};
    for (let key in newData) {
        if (newData[key] !== "" && String(newData[key]) !== String(originalData[key])) {
            changedData[key] = newData[key];
        }
    }
    
    if (Object.keys(changedData).length === 0) {
        document.getElementById("updateMsg").style.color = "green";
        document.getElementById("updateMsg").textContent = "No changes made.";
        return;
    }
    
    fetch('/HR/update_employee', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            employee_id: employeeId,
            updated_data: changedData
        })
    })
    .then(response => response.json())
    .then(data => {
        let updateMsg = document.getElementById("updateMsg");
        if (data.success) {
            updateMsg.style.color = "green";
            updateMsg.textContent = data.success;
        } else if (data.error) {
            updateMsg.style.color = "red";
            updateMsg.textContent = data.error;
        }
    })
    .catch(error => {
        console.error("Error updating employee:", error);
        document.getElementById("updateMsg").style.color = "red";
        document.getElementById("updateMsg").textContent = "Error updating employee.";
    });
}
