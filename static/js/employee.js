

document.addEventListener("DOMContentLoaded", function() {
    // Immediately fetch employee details once the DOM is loaded.
    fetch("/employee/details")
        .then(response => response.json())
        .then(data => {
            let details = `
                <h3>Employee Details</h3>
                <p><strong>ID:</strong> ${data.E_id}</p>
                <p><strong>Name:</strong> ${data.E_name}</p>
                <p><strong>Designation:</strong> ${data.Designation}</p>
                <p><strong>Department:</strong> ${data.Department}</p>
                <p><strong>Gross Salary:</strong> ${data.Gross_salary}</p>
                <p><strong>Deductible:</strong> ${data.Deductable}</p>
                <p><strong>Net Salary:</strong> ${data.Net_Salary}</p>
            `;
            document.getElementById("employeeDetails").innerHTML = details;
        })
        .catch(error => console.error("Error fetching employee details:", error));
});
