document.addEventListener("DOMContentLoaded", () => {
    // Smooth scrolling for navigation links
    document.querySelectorAll('.nav-links a').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                window.scrollTo({
                    top: targetSection.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Launch App button logic - Remove default redirect and rely on smooth scroll
    const launchBtns = document.querySelectorAll('.btn-primary, .btn-glow');
    launchBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const targetId = btn.getAttribute('href');
            if(targetId && targetId.startsWith('#')) return; // handled by smooth scroll
        });
    });

    // Form Submission Logic
    const form = document.getElementById('prediction-form');
    if (form) {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = document.getElementById('submit-btn');
            submitBtn.textContent = 'Processing...';
            submitBtn.disabled = true;

            const data = {
                age: document.getElementById('age').value,
                gender: document.getElementById('gender').value,
                hormonal: document.getElementById('hormonal').value,
                body_weight: document.getElementById('body_weight').value,
                family_history: document.getElementById('family_history').value,
                prior_fracture: document.getElementById('prior_fracture').value,
                calcium: document.getElementById('calcium').value,
                vitamin_d: document.getElementById('vitamin_d').value,
                physical: document.getElementById('physical').value,
                smoking: document.getElementById('smoking').value
            };

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                const display = document.getElementById('result-display');
                const title = document.getElementById('result-title');
                const desc = document.getElementById('result-desc');
                const progress = document.getElementById('risk-progress');
                
                display.style.display = 'block';
                
                if (result.status === 'success') {
                    progress.style.width = result.risk_pct + '%';
                    
                    if (result.prediction === 1) {
                        title.textContent = '⚠️ High Risk (' + result.risk_pct + '%)';
                        title.style.color = '#ff5f56';
                        progress.style.background = '#ff5f56';
                        desc.textContent = 'Please consult a specialist and consider a bone density test.';
                    } else {
                        title.textContent = '✅ Low Risk (' + result.risk_pct + '%)';
                        title.style.color = '#27c93f';
                        progress.style.background = '#27c93f';
                        desc.textContent = 'Maintain your healthy lifestyle with regular exercise and balanced diet.';
                    }
                } else {
                    title.textContent = 'Error';
                    desc.textContent = result.message || 'Something went wrong.';
                    title.style.color = '#ffbd2e';
                    progress.style.width = '0%';
                }
            } catch (error) {
                alert('Error making prediction. Check console for details.');
                console.error(error);
            } finally {
                submitBtn.textContent = 'Predict Risk';
                submitBtn.disabled = false;
            }
        });
    }

    // Add scroll animations for elements
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = 1;
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.feature-card, .step').forEach((el) => {
        el.style.opacity = 0;
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
});
