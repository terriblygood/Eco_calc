console.log("Калькулятор TerryOne инициализирован");

// Функция анимации прогресс-баров
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach((bar) => {
        // Получаем оригинальную ширину из атрибута data-width или из стиля
        const targetWidth = bar.getAttribute('data-width') || bar.style.width;
        
        // Сохраняем оригинальную ширину для будущего использования
        if (!bar.getAttribute('data-width')) {
            bar.setAttribute('data-width', targetWidth);
        }
        
        // Сначала устанавливаем ширину 0
        bar.style.width = '0%';
        
        // Затем возвращаем к целевой ширине (анимация)
        setTimeout(() => {
            bar.style.width = targetWidth;
        }, 100);
    });
}

// Обработка нажатия на кнопку расчета
function setupCalculateButton() {
    const calculateBtn = document.getElementById('calculate-payback-btn');
    if (calculateBtn) {
        calculateBtn.addEventListener('click', () => {
            calculateBtn.classList.add("calm-click");
            setTimeout(() => {
                calculateBtn.classList.remove("calm-click");
            }, 500);
            
            // Запускаем анимацию через 1 секунду после нажатия
            setTimeout(animateProgressBars, 1000);
        });
    }
}

// Наблюдаем за изменениями в DOM для обнаружения появления прогресс-баров
function setupMutationObserver() {
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                const hasProgressBars = document.querySelector('.progress-bar') !== null;
                if (hasProgressBars) {
                    animateProgressBars();
                }
            }
        });
    });
    
    const savingsVisualizer = document.getElementById('savings-visualizer');
    if (savingsVisualizer) {
        observer.observe(savingsVisualizer, { childList: true, subtree: true });
    }
}

// Инициализация скрипта
function init() {
    setupCalculateButton();
    setupMutationObserver();
}

// Запускаем инициализацию при загрузке DOM
document.addEventListener('DOMContentLoaded', init);

// Дополнительная проверка, если DOM загружен до запуска скрипта
if (document.readyState === 'interactive' || document.readyState === 'complete') {
    init();
} 