console.log("Калькулятор TerryOne инициализирован");

// Функция для анимации прогресс-баров
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.savings-visualizer .progress-bar');
    
    progressBars.forEach(bar => {
        // Сохраняем целевую ширину
        const targetWidth = bar.style.width;
        // Сначала устанавливаем ширину в 0%
        bar.style.width = '0%';
        
        // Добавляем небольшую задержку перед запуском анимации
        setTimeout(() => {
            bar.style.width = targetWidth;
        }, 100);
    });
}

// Функция для добавления эффекта клика на кнопку
function addButtonClickEffect() {
    const calculateButton = document.getElementById('calculate-payback-btn');
    
    if (calculateButton) {
        calculateButton.addEventListener('click', function() {
            this.classList.add('calm-click');
            
            // Удаляем класс после завершения анимации
            setTimeout(() => {
                this.classList.remove('calm-click');
            }, 500);
            
            // Анимируем прогресс-бары после небольшой задержки
            setTimeout(() => {
                animateProgressBars();
                animateResults();
            }, 800);
        });
    }
}

// Функция для анимации появления результатов
function animateResults() {
    const resultRows = document.querySelectorAll('.result-row');
    
    resultRows.forEach((row, index) => {
        row.style.opacity = '0';
        setTimeout(() => {
            row.style.opacity = '1';
        }, 100 * (index + 1));
    });
}

// Настройка MutationObserver для наблюдения за изменениями в DOM
function setupMutationObserver() {
    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            if (mutation.addedNodes.length > 0) {
                // Проверяем, был ли добавлен элемент с классом savings-visualizer
                const addedVisualizer = Array.from(mutation.addedNodes).some(node => {
                    return node.classList && node.classList.contains('savings-visualizer');
                });
                
                if (addedVisualizer) {
                    // Запускаем анимацию
                    setTimeout(() => {
                        animateProgressBars();
                        animateResults();
                    }, 200);
                }
            }
        });
    });
    
    // Настраиваем наблюдение за изменениями в DOM
    observer.observe(document.body, { childList: true, subtree: true });
}

// Инициализация всех функций при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('Калькулятор TerryONE загружен');
    setupForm();
    setupAnimations();
    addButtonClickEffect();
    setupMutationObserver();
    
    // Рассчитываем результаты с базовыми значениями при загрузке страницы
    setTimeout(() => {
        const hotelRooms = parseInt(document.getElementById('hotelRooms').value) || 100;
        const avgOccupancy = parseInt(document.getElementById('avgOccupancy').value) || 70;
        const towelsPerRoom = parseInt(document.getElementById('towelsPerRoom').value) || 4;
        const replacementPolicy = parseInt(document.getElementById('towelReplacementPolicy').value) || 1;
        
        calculateResults(hotelRooms, avgOccupancy, towelsPerRoom, replacementPolicy);
        console.log("Выполнен автоматический расчет с базовыми значениями");
    }, 500);
    
    // Если визуализатор уже присутствует при загрузке страницы
    if (document.querySelector('.savings-visualizer')) {
        setTimeout(() => {
            animateProgressBars();
            animateResults();
        }, 500);
    }
});

// Дополнительная проверка, если DOM загружен до запуска скрипта
if (document.readyState === 'interactive' || document.readyState === 'complete') {
    init();
}

// Настройка формы калькулятора
function setupForm() {
    const calculatorForm = document.getElementById('calculatorForm');
    
    if (calculatorForm) {
        calculatorForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Получение данных из формы
            const hotelRooms = parseInt(document.getElementById('hotelRooms').value) || 0;
            const avgOccupancy = parseInt(document.getElementById('avgOccupancy').value) || 0;
            const towelsPerRoom = parseInt(document.getElementById('towelsPerRoom').value) || 0;
            const replacementPolicy = parseInt(document.getElementById('towelReplacementPolicy').value) || 1;
            
            // Проверка введенных данных
            if (hotelRooms <= 0 || avgOccupancy <= 0 || towelsPerRoom <= 0) {
                alert('Пожалуйста, введите корректные значения больше нуля');
                return;
            }
            
            // Расчет результатов
            calculateResults(hotelRooms, avgOccupancy, towelsPerRoom, replacementPolicy);
            
            // Применение эффекта нажатия к кнопке
            const submitButton = document.querySelector('button[type="submit"]');
            applyClickEffect(submitButton);
        });
        
        // Обработчик сброса формы
        const resetButton = calculatorForm.querySelector('button[type="reset"]');
        if (resetButton) {
            resetButton.addEventListener('click', function() {
                // Скрываем визуализатор при сбросе формы
                document.getElementById('savingsVisualizer').style.display = 'none';
                applyClickEffect(this);
            });
        }
    }
}

// Расчет и отображение результатов
function calculateResults(hotelRooms, avgOccupancy, towelsPerRoom, replacementPolicy) {
    // Базовые расчеты по формулам TowelCalculator
    const occupancyFraction = avgOccupancy / 100;
    const daysPerYear = 365;
    
    // Расчет числа циклов стирки в год (cycles_per_year)
    // По формуле из TowelCalculator.cycles_per_year
    let washInterval = 1; // по умолчанию ежедневно
    switch (replacementPolicy) {
        case 1: // Ежедневно
            washInterval = 1;
            break;
        case 2: // Каждые 2 дня
            washInterval = 2;
            break;
        case 3: // По запросу гостя
            washInterval = 3.5; // В среднем раз в 3-4 дня
            break;
    }
    
    const totalTowels = hotelRooms * towelsPerRoom;
    const occupiedRoomsPerDay = Math.round(hotelRooms * occupancyFraction);
    
    // Стирки в год = (комнаты * загрузка * полотенец на комнату * дней в году) / интервал стирки
    const cyclesPerYear = Math.round((occupiedRoomsPerDay * towelsPerRoom * daysPerYear) / washInterval);
    
    // Срок службы полотенец
    // Стандартное хлопковое полотенце - 100-120 циклов
    // Гибридное (TerryONE) - 200-250 циклов
    const cottonCycles = 110; // Среднее число циклов до износа
    const hybridCycles = 225; // Среднее число циклов до износа
    
    // Срок службы в годах (lifespan_years)
    const cottonLifespanYears = cottonCycles / (cyclesPerYear / totalTowels);
    const hybridLifespanYears = hybridCycles / (cyclesPerYear / totalTowels);
    
    // Количество замен полотенец в год
    const cottonReplacementsPerYear = totalTowels / cottonLifespanYears;
    const hybridReplacementsPerYear = totalTowels / hybridLifespanYears;
    
    // Экономия на заменах в год
    const replacementsSaved = Math.round(cottonReplacementsPerYear - hybridReplacementsPerYear);
    
    // Стоимость одного цикла стирки
    const waterCostPerCycle = 0.04; // м³ на цикл
    const energyCostPerCycle = 0.65; // кВт*ч на цикл (средне)
    const co2PerCycle = 0.35; // кг CO₂ на цикл
    
    // Вес хлопкового полотенца - 600г, гибридного - 450г
    const cottonWeight = 0.6; // кг
    const hybridWeight = 0.45; // кг
    
    // Экономия ресурсов
    // Экономия воды учитывает разницу в весе полотенец и количество стирок
    const waterSaved = Math.round(cyclesPerYear * waterCostPerCycle * (1 - (hybridWeight / cottonWeight)) * 1000); // литры
    
    // Экономия энергии учитывает разницу в весе и температуре стирки (хлопок - 60°C, гибридное - 40°C)
    const energyTemp = 1.5; // коэффициент экономии от снижения температуры
    const energySaved = Math.round(cyclesPerYear * energyCostPerCycle * (1 - (hybridWeight / cottonWeight) / energyTemp));
    
    // Сокращение выбросов CO₂
    const co2Saved = Math.round(cyclesPerYear * co2PerCycle * (1 - (hybridWeight / cottonWeight)));
    
    // Экономия денег:
    // 1. На замене полотенец
    const cottonCost = 450; // Средняя стоимость хлопкового полотенца
    const hybridCost = 700; // Средняя стоимость гибридного полотенца
    const replacementCostSaved = Math.round((cottonCost * cottonReplacementsPerYear) - (hybridCost * hybridReplacementsPerYear));
    
    // 2. На ресурсах
    const waterCostPerLiter = 0.05; // рублей за литр
    const energyCostPerKWh = 4.5; // рублей за кВт*ч
    
    const resourceCostSaved = Math.round(
        (waterSaved * waterCostPerLiter) + 
        (energySaved * energyCostPerKWh)
    );
    
    // Общая экономия
    const costSaved = replacementCostSaved + resourceCostSaved;
    
    // Вывод информации о расчетах для отладки
    console.log("=== РАСЧЕТЫ ЭКОНОМИИ ОТ ПОЛОТЕНЕЦ TERRYONE ===");
    console.log("Исходные данные:");
    console.log(`- Количество номеров: ${hotelRooms}`);
    console.log(`- Средняя загрузка отеля: ${avgOccupancy}%`);
    console.log(`- Полотенец на номер: ${towelsPerRoom}`);
    console.log(`- Интервал замены: ${washInterval} дней`);
    console.log("\nПромежуточные расчеты:");
    console.log(`- Общее количество полотенец: ${totalTowels}`);
    console.log(`- Занятых номеров в день: ${occupiedRoomsPerDay}`);
    console.log(`- Циклов стирки в год: ${cyclesPerYear}`);
    console.log(`- Срок службы хлопковых полотенец: ${cottonLifespanYears.toFixed(2)} лет`);
    console.log(`- Срок службы гибридных полотенец: ${hybridLifespanYears.toFixed(2)} лет`);
    console.log(`- Замены хлопковых полотенец в год: ${cottonReplacementsPerYear.toFixed(2)}`);
    console.log(`- Замены гибридных полотенец в год: ${hybridReplacementsPerYear.toFixed(2)}`);
    console.log("\nРезультаты экономии:");
    console.log(`- Экономия на заменах: ${replacementsSaved} полотенец в год`);
    console.log(`- Экономия воды: ${waterSaved} литров`);
    console.log(`- Экономия энергии: ${energySaved} кВт*ч`);
    console.log(`- Сокращение CO₂: ${co2Saved} кг`);
    console.log(`- Экономия на заменах: ${replacementCostSaved} ₽`);
    console.log(`- Экономия на ресурсах: ${resourceCostSaved} ₽`);
    console.log(`- Общая экономия: ${costSaved} ₽`);
    
    // Форматирование чисел для отображения
    const formattedWaterSaved = formatNumber(waterSaved);
    const formattedEnergySaved = formatNumber(energySaved);
    const formattedCO2Saved = formatNumber(co2Saved);
    const formattedCostSaved = formatNumber(costSaved);
    const formattedReplacementsSaved = formatNumber(replacementsSaved);
    
    // Обновление значений в интерфейсе
    document.getElementById('energySaved').textContent = formattedEnergySaved;
    document.getElementById('waterSaved').textContent = formattedWaterSaved;
    document.getElementById('costSaved').textContent = formattedCostSaved;
    document.getElementById('co2Saved').textContent = formattedCO2Saved;
    document.getElementById('replacementsSaved').textContent = formattedReplacementsSaved;
    
    // Отображение визуализатора
    const savingsVisualizer = document.getElementById('savingsVisualizer');
    savingsVisualizer.style.display = 'block';
    
    // Рассчитываем проценты для прогресс-баров на основе эффективности
    // Экономия воды - до 40% максимум
    const waterPercent = Math.min(Math.round((waterSaved / (cyclesPerYear * waterCostPerCycle * 1000)) * 100), 40);
    
    // Экономия энергии - до 50% максимум
    const energyPercent = Math.min(Math.round((energySaved / (cyclesPerYear * energyCostPerCycle)) * 100), 50);
    
    // Экономия денег - до 30% от общих затрат
    const totalCost = (cottonCost * cottonReplacementsPerYear) + 
                      (cyclesPerYear * waterCostPerCycle * 1000 * waterCostPerLiter) + 
                      (cyclesPerYear * energyCostPerCycle * energyCostPerKWh);
    
    const costPercent = Math.min(Math.round((costSaved / totalCost) * 100), 30);
    
    // CO2 - до 40% максимум
    const co2Percent = Math.min(Math.round((co2Saved / (cyclesPerYear * co2PerCycle)) * 100), 40);
    
    // Замены - до 50% максимум (сокращение числа замен)
    const replacementsPercent = Math.min(Math.round((replacementsSaved / cottonReplacementsPerYear) * 100), 50);
    
    // Запуск анимации прогресс-баров
    animateProgressBar('energyBar', energyPercent);
    animateProgressBar('waterBar', waterPercent);
    animateProgressBar('costBar', costPercent);
    animateProgressBar('co2Bar', co2Percent);
    animateProgressBar('replacementBar', replacementsPercent);
    
    // Прокрутка к результатам
    setTimeout(() => {
        savingsVisualizer.scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

// Функция для форматирования числа с разделителями тысяч
function formatNumber(number) {
    return number.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

// Функция для анимации прогресс-бара
function animateProgressBar(elementId, targetPercent) {
    const progressBar = document.getElementById(elementId);
    if (!progressBar) return;
    
    // Сбрасываем текущую ширину
    progressBar.style.width = '0%';
    
    // Запускаем анимацию с небольшой задержкой
    setTimeout(() => {
        progressBar.style.width = targetPercent + '%';
    }, 200);
}

// Функция для применения эффекта нажатия кнопки
function applyClickEffect(button) {
    button.classList.add('btn-click-effect');
    setTimeout(() => {
        button.classList.remove('btn-click-effect');
    }, 300);
}

// Настройка анимаций
function setupAnimations() {
    // Добавляем эффект клика для всех кнопок
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('mousedown', function() {
            this.classList.add('btn-click-effect');
        });
        
        button.addEventListener('mouseup', function() {
            this.classList.remove('btn-click-effect');
        });
        
        button.addEventListener('mouseleave', function() {
            this.classList.remove('btn-click-effect');
        });
    });
    
    // Анимация результатов при прокрутке
    const resultRows = document.querySelectorAll('.result-row');
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        resultRows.forEach(row => {
            observer.observe(row);
        });
    } else {
        // Для браузеров без поддержки IntersectionObserver
        resultRows.forEach(row => {
            row.style.opacity = '1';
        });
    }
} 