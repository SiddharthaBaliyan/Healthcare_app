/* ===============================
   Heart Disease Predictor JS
   =============================== */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('predictionForm');
    const submitBtn = document.getElementById('submitBtn');
    const resultSection = document.getElementById('resultSection');
    const resultCard = document.getElementById('resultCard');

    // Check API status on page load
    checkApiStatus();

    // Set up form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        await makePrediction();
    });

    /**
     * Check API Health Status
     */
    async function checkApiStatus() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            
            const statusBadge = document.getElementById('api-status');
            const footerStatus = document.getElementById('footer-api-status');
            
            if (data.api.status === 'healthy' && data.api.model_loaded) {
                statusBadge.innerHTML = '<i class="fas fa-circle"></i> API Connected';
                statusBadge.className = 'badge bg-success ms-2';
                footerStatus.className = 'badge bg-success';
                footerStatus.textContent = 'Connected';
            } else {
                statusBadge.innerHTML = '<i class="fas fa-circle"></i> API Error';
                statusBadge.className = 'badge bg-warning ms-2';
                footerStatus.className = 'badge bg-warning';
                footerStatus.textContent = 'Disconnected';
                
                if (!data.api.model_loaded) {
                    showAlert('Model not loaded. Please run the training pipeline first.', 'warning');
                }
            }
        } catch (error) {
            console.error('Error checking API status:', error);
            const statusBadge = document.getElementById('api-status');
            statusBadge.innerHTML = '<i class="fas fa-circle"></i> API Error';
            statusBadge.className = 'badge bg-danger ms-2';
            
            showAlert('Cannot connect to API server. Make sure it\'s running on port 8000.', 'danger');
        }
    }

    /**
     * Make Prediction
     */
    async function makePrediction() {
        // Validate form
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return;
        }

        // Get form data
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="loading"></span> Processing...';

        try {
            // Send prediction request
            const response = await fetch('/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                displayResult(result.data);
            } else {
                showAlert(`Error: ${result.error}`, 'danger');
            }
        } catch (error) {
            console.error('Prediction error:', error);
            showAlert('An error occurred while making the prediction. Please try again.', 'danger');
        } finally {
            // Reset button state
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fas fa-magic"></i> Get Prediction';
        }
    }

    /**
     * Display Result
     */
    function displayResult(data) {
        const isPossitive = data.prediction === 'Presence';
        const icon = isPossitive ? 'fa-exclamation-circle' : 'fa-check-circle';
        const iconClass = isPossitive ? 'danger' : 'success';
        const cardClass = isPossitive ? 'result-danger' : 'result-success';
        const backgroundColor = isPossitive ? '#FFE6E6' : '#E6F7F5';

        const resultHTML = `
            <div class="result-card ${cardClass}" style="background: ${backgroundColor}">
                <div class="result-header">
                    <div class="result-icon ${iconClass}">
                        <i class="fas ${icon}"></i>
                    </div>
                    <div>
                        <h3 class="result-title">${data.prediction}</h3>
                        <p class="result-subtitle">Heart Disease Prediction Result</p>
                    </div>
                </div>

                <div class="result-confidence">
                    <div class="confidence-label">
                        <i class="fas fa-chart-pie"></i> Confidence Level
                    </div>
                    <div class="confidence-bar">
                        <div class="confidence-progress" style="width: 0%;" data-width="${data.confidence}"></div>
                    </div>
                    <div class="confidence-percent">${data.confidence.toFixed(2)}%</div>
                </div>

                <div class="result-message">
                    ${data.message}
                </div>

                <div class="result-details">
                    <h5>Prediction Details</h5>
                    <dl class="row">
                        <dt class="col-sm-4">Prediction:</dt>
                        <dd class="col-sm-8">
                            <strong>${data.prediction}</strong>
                        </dd>
                        
                        <dt class="col-sm-4">Probability:</dt>
                        <dd class="col-sm-8">
                            ${(data.probability * 100).toFixed(2)}%
                        </dd>
                        
                        <dt class="col-sm-4">Confidence:</dt>
                        <dd class="col-sm-8">
                            ${data.confidence.toFixed(2)}%
                        </dd>
                    </dl>
                </div>

                <div class="alert alert-info mt-3">
                    <i class="fas fa-info-circle"></i> <strong>Note:</strong> This is an AI-powered prediction for informational purposes. 
                    Please consult with a qualified healthcare professional for accurate medical diagnosis and treatment.
                </div>

                <div class="d-grid gap-2 mt-3">
                    <button type="button" class="btn btn-outline-primary" onclick="downloadResult('${data.prediction}', ${data.confidence})">
                        <i class="fas fa-download"></i> Download Result
                    </button>
                </div>
            </div>
        `;

        resultCard.innerHTML = resultHTML;
        resultSection.style.display = 'block';

        // Animate confidence bar
        setTimeout(() => {
            const progressBar = resultCard.querySelector('.confidence-progress');
            progressBar.style.width = progressBar.dataset.width + '%';
        }, 100);

        // Scroll to result
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    /**
     * Show Alert
     */
    window.showAlert = function(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.style.marginTop = '1rem';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Insert alert at the top of the prediction section
        const predictionSection = document.querySelector('.prediction-section');
        predictionSection.insertBefore(alertDiv, predictionSection.firstChild);

        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    };

    /**
     * Download Result
     */
    window.downloadResult = function(prediction, confidence) {
        // Create result text
        const resultText = `
Heart Disease Prediction Report
================================
Generated: ${new Date().toLocaleString()}

PREDICTION RESULT: ${prediction}
Confidence Level: ${confidence.toFixed(2)}%

Patient Information:
${getFormDataForReport()}

================================
Disclaimer: This prediction is for informational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment.
        `;

        // Create blob and download
        const blob = new Blob([resultText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `heart-disease-prediction-${new Date().getTime()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        showAlert('Report downloaded successfully!', 'success');
    };

    /**
     * Get Form Data for Report
     */
    function getFormDataForReport() {
        const formData = new FormData(form);
        let text = '';
        
        const labelMap = {
            'Age': 'Age (years)',
            'Sex': 'Sex',
            'Chest_pain_type': 'Chest Pain Type',
            'BP': 'Blood Pressure (mmHg)',
            'Cholesterol': 'Cholesterol (mg/dl)',
            'FBS_over_120': 'Fasting Blood Sugar > 120',
            'EKG_results': 'EKG Results',
            'Max_HR': 'Max Heart Rate',
            'Exercise_angina': 'Exercise Induced Angina',
            'ST_depression': 'ST Depression',
            'Slope_of_ST': 'Slope of ST Segment',
            'Number_of_vessels_fluro': 'Number of Vessels',
            'Thallium': 'Thallium Value'
        };

        for (const [key, value] of formData) {
            const label = labelMap[key] || key;
            text += `${label}: ${value}\n`;
        }

        return text;
    }

    /**
     * Real-time form validation
     */
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('change', () => {
            if (input.value) {
                input.classList.remove('is-invalid');
            }
        });

        input.addEventListener('input', () => {
            // Validate number ranges
            if (input.type === 'number') {
                const min = parseFloat(input.min);
                const max = parseFloat(input.max);
                const value = parseFloat(input.value);

                if (value < min || value > max) {
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            }
        });
    });

    /**
     * Refresh API Status
     */
    setInterval(checkApiStatus, 30000); // Check every 30 seconds
});

/**
 * Format number with thousand separator
 */
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

/**
 * Get browser geolocation
 */
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        console.log("Geolocation is not supported by this browser.");
    }
}

function showPosition(position) {
    console.log("Latitude: " + position.coords.latitude);
    console.log("Longitude: " + position.coords.longitude);
}
