document.addEventListener("DOMContentLoaded", function () {

    // =====================================================
    // START PREDICTION BUTTON
    // =====================================================

    const predictBtn = document.getElementById("predictBtn");

    if (predictBtn) {
        predictBtn.addEventListener("click", function () {
            window.location.href = "a.html";
        });
    }


    // =====================================================
    // PREDICTION FORM
    // =====================================================

    const form = document.getElementById("predictionForm");

    if (!form) {
        console.error("predictionForm not found.");
        return;
    }


    form.addEventListener("submit", async function (event) {

        event.preventDefault();


        // =================================================
        // GET ALL INPUTS AND SELECTS
        // =================================================

        const fields = form.querySelectorAll(
            "input, select"
        );


        console.log(
            "Number of form fields:",
            fields.length
        );


        // Your form must contain 13 fields
        if (fields.length < 13) {

            alert(
                "Error: Expected 13 input fields, but found " +
                fields.length
            );

            return;
        }


        // =================================================
        // CHECK EMPTY FIELDS
        // =================================================

        for (let i = 0; i < 13; i++) {

            if (fields[i].value === "") {

                alert(
                    "Please fill/select all fields."
                );

                fields[i].focus();

                return;
            }
        }


        // =================================================
        // GET VALUES IN MODEL ORDER
        // =================================================

        const formData = {

            age: fields[0].value,

            sex: fields[1].value,

            cp: fields[2].value,

            trestbps: fields[3].value,

            chol: fields[4].value,

            fbs: fields[5].value,

            restecg: fields[6].value,

            thalach: fields[7].value,

            exang: fields[8].value,

            oldpeak: fields[9].value,

            slope: fields[10].value,

            ca: fields[11].value,

            thal: fields[12].value
        };


        console.log(
            "DATA SENT TO FLASK:"
        );

        console.log(formData);


        // =================================================
        // SEND TO FLASK
        // =================================================

        try {

            const response = await fetch(
                "http://127.0.0.1:5000/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(formData)
                }
            );


            // =================================================
            // READ SERVER RESPONSE
            // =================================================

            const result =
                await response.json();


            console.log(
                "FLASK RESPONSE:",
                result
            );


            // =================================================
            // ERROR FROM FLASK
            // =================================================

            if (!response.ok ||
                result.success === false) {

                alert(
                    result.error ||
                    "Prediction failed."
                );

                return;
            }


            // =================================================
            // SHOW RESULT
            // =================================================

            showResult(
                result.prediction,
                result.risk_percentage
            );


        } catch (error) {

            console.error(
                "Connection error:",
                error
            );


            alert(
                "Cannot connect to Flask server.\n\n" +
                "Make sure app.py is running at:\n" +
                "http://127.0.0.1:5000"
            );

        }

    });

});


// =========================================================
// SHOW RESULT
// =========================================================

function showResult(
    prediction,
    riskPercentage
) {

    const modal =
        document.getElementById("resultModal");

    const title =
        document.getElementById("modalTitle");

    const description =
        document.getElementById(
            "modalDescription"
        );

    const icon =
        document.getElementById("riskIcon");


    // =====================================================
    // IF MODAL DOES NOT EXIST
    // =====================================================

    if (!modal) {

        if (Number(prediction) === 0) {

            alert(
                "LOW RISK\n\n" +
                "Estimated Risk: " +
                Number(riskPercentage).toFixed(2) +
                "%"
            );

        } else {

            alert(
                "HIGH RISK\n\n" +
                "Estimated Risk: " +
                Number(riskPercentage).toFixed(2) +
                "%"
            );
        }

        return;
    }


    // =====================================================
    // LOW RISK
    // =====================================================

    if (Number(prediction) === 0) {

        title.textContent =
            "Low Risk Detected";

        title.style.color =
            "#2ecc71";


        icon.innerHTML =
            `
            <i
                class="fa-solid fa-circle-check"
                style="
                    color:#2ecc71;
                    font-size:55px;
                "
            ></i>
            `;


        description.innerHTML =
            `
            <div>

                <h3>🟢 Low Risk</h3>

                <p>
                    The model classified this
                    input as <strong>Low Risk</strong>.
                </p>

                <p>
                    Estimated Risk:
                    <strong>
                        ${Number(riskPercentage).toFixed(2)}%
                    </strong>
                </p>

                <small>
                    This is a machine-learning
                    prediction for demonstration
                    purposes and is not a medical diagnosis.
                </small>

            </div>
            `;

    }


    // =====================================================
    // HIGH RISK
    // =====================================================

    else {

        title.textContent =
            "High Risk Detected";

        title.style.color =
            "#e74c3c";


        icon.innerHTML =
            `
            <i
                class="fa-solid fa-triangle-exclamation"
                style="
                    color:#e74c3c;
                    font-size:55px;
                "
            ></i>
            `;


        description.innerHTML =
            `
            <div>

                <h3>🔴 High Risk</h3>

                <p>
                    The model classified this
                    input as <strong>High Risk</strong>.
                </p>

                <p>
                    Estimated Risk:
                    <strong>
                        ${Number(riskPercentage).toFixed(2)}%
                    </strong>
                </p>

                <small>
                    This is a machine-learning
                    prediction for demonstration
                    purposes and is not a medical diagnosis.
                </small>

            </div>
            `;

    }


    // =====================================================
    // OPEN MODAL
    // =====================================================

    modal.style.display = "flex";
}


// =========================================================
// CLOSE MODAL
// =========================================================

function closeModal() {

    const modal =
        document.getElementById("resultModal");

    if (modal) {

        modal.style.display = "none";

    }
}


// =========================================================
// CLOSE MODAL BY CLICKING OUTSIDE
// =========================================================

window.addEventListener(
    "click",
    function (event) {

        const modal =
            document.getElementById("resultModal");

        if (
            modal &&
            event.target === modal
        ) {

            modal.style.display = "none";
        }

    }
);