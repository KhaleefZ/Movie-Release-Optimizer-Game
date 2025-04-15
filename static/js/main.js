// Form Handling
document.addEventListener('DOMContentLoaded', function() {
    // Budget and Marketing Budget Sliders
    function initializeSliders() {
        const budgetSlider = document.getElementById('budget_slider');
        const budgetInput = document.getElementById('budget_input');
        const budgetDisplay = document.getElementById('budget_display');
        const marketingSlider = document.getElementById('marketing_slider');
        const marketingInput = document.getElementById('marketing_input');
        const marketingDisplay = document.getElementById('marketing_display');

        if (budgetSlider && budgetInput && budgetDisplay) {
            budgetSlider.addEventListener('input', function() {
                const value = parseInt(this.value);
                budgetInput.value = value;
                budgetDisplay.textContent = value;
                updateMarketingMax(value);
            });
        }

        if (marketingSlider && marketingInput && marketingDisplay) {
            marketingSlider.addEventListener('input', function() {
                const value = parseInt(this.value);
                marketingInput.value = value;
                marketingDisplay.textContent = value;
            });
        }
    }

    function updateMarketingMax(budgetValue) {
        const marketingSlider = document.getElementById('marketing_slider');
        const marketingInput = document.getElementById('marketing_input');
        const marketingDisplay = document.getElementById('marketing_display');
        
        if (marketingSlider && marketingInput && marketingDisplay) {
            const maxMarketing = Math.min(200, Math.floor(budgetValue * 0.5));
            marketingSlider.max = maxMarketing;
            
            const currentValue = parseInt(marketingInput.value);
            if (currentValue > maxMarketing) {
                marketingInput.value = maxMarketing;
                marketingSlider.value = maxMarketing;
                marketingDisplay.textContent = maxMarketing;
            }
        }
    }

    // Month Selection in Calendar
    function initializeCalendar() {
        const monthButtons = document.querySelectorAll('.month-button');
        monthButtons.forEach(button => {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                monthButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // Show date selection after month is selected
                const dateSelection = document.querySelector('.date-selection');
                if (dateSelection) {
                    dateSelection.classList.remove('d-none');
                    dateSelection.classList.add('fade-in');
                }
            });
        });
    }

    // Charts Animation
    document.addEventListener('DOMContentLoaded', function() {
        // Add animation classes to elements
        document.querySelectorAll('.card').forEach(card => {
            card.classList.add('animate-fade-in');
        });

        // Initialize tooltips
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });

        // Add hover effects to charts
        const charts = document.querySelectorAll('.chart-container');
        charts.forEach(chart => {
            chart.addEventListener('mouseover', function() {
                this.style.transform = 'scale(1.02)';
                this.style.transition = 'transform 0.3s ease';
            });
            chart.addEventListener('mouseout', function() {
                this.style.transform = 'scale(1)';
            });
        });

        // Progress bar animation
        document.querySelectorAll('.progress-bar').forEach(bar => {
            const value = bar.getAttribute('aria-valuenow');
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = value + '%';
                bar.style.transition = 'width 1s ease-in-out';
            }, 200);
        });
    });

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    initializeCalendar();
    initializeCharts();
});

// Toast Notifications
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
    container.appendChild(toast);
    document.body.appendChild(container);
    
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    
    toast.addEventListener('hidden.bs.toast', function () {
        container.remove();
    });
}


function updateBudgetValue(val) {
    const value = Math.min(Math.max(parseInt(val), 1), 500);
    document.getElementById('budget_input').value = value;
    document.getElementById('budget_display').textContent = value;
    updateMarketingMax(value); // Update marketing budget constraints
}

function updateMarketingValue(val) {
    const value = Math.min(Math.max(parseInt(val), 1), 200);
    const maxMarketing = Math.min(200, Math.floor(document.getElementById('budget_input').value * 0.5));
    const finalValue = Math.min(value, maxMarketing);
    
    document.getElementById('marketing_input').value = finalValue;
    document.getElementById('marketing_display').textContent = finalValue;
}

function calculateROI(boxOffice, totalCost) {
    if (totalCost === 0) return 0;
    return ((boxOffice - totalCost) / totalCost * 100).toFixed(1);
}

// Remove the updateMarketingSlider function as it's no longer needed

document.addEventListener('DOMContentLoaded', function() {
    // Handle reset button
    const resetButton = document.getElementById('resetButton');
    if (resetButton) {
        resetButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Submit the form with reset_date
            const form = document.getElementById('dateForm');
            const resetInput = document.createElement('input');
            resetInput.type = 'hidden';
            resetInput.name = 'reset_date';
            resetInput.value = 'true';
            form.appendChild(resetInput);
            form.submit();
            
            // Clear active states
            document.querySelectorAll('.month-button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Reset date select if it exists
            const dateSelect = document.getElementById('release_date');
            if (dateSelect) {
                dateSelect.selectedIndex = 0;
            }
        });
    }
    
    // Handle month selection
    const monthButtons = document.querySelectorAll('.month-button');
    monthButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            window.location.href = this.href;
        });
    });
});