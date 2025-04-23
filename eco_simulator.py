import dash
from dash import dcc, html, Input, Output, callback, State, no_update
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import math
import time

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "TerryOne Eco Dynamics"

# Добавляем стили через index_string
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');
            
            body {
                font-family: 'Montserrat', sans-serif;
                background-color: #fff;
                color: #333;
                margin: 0;
                padding: 0;
            }
            
            .terryOne-container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 15px;
            }
            
            .terryOne-header {
                background-color: white;
                text-align: center;
                padding: 30px 0 10px;
                border-bottom: 1px solid #f0f0f0;
                margin-bottom: 20px;
            }
            
            .terryOne-logo {
                font-weight: 700;
                color: #333;
                text-transform: lowercase;
                font-size: 2.4rem;
                letter-spacing: 1px;
                margin-bottom: 5px;
                display: inline-block;
            }
            
            .terryOne-logo span {
                color: #777;
                font-weight: 400;
            }
            
            .terryOne-tagline {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                gap: 15px;
                margin: 15px 0;
            }
            
            .terryOne-tag {
                font-weight: 600;
                color: #333;
                font-size: 0.75rem;
                letter-spacing: 0.5px;
            }
            
            .page-header {
                text-align: center;
                margin: 20px 0 40px;
                text-transform: uppercase;
                font-weight: 600;
                color: #333;
                font-size: 1.3rem;
                letter-spacing: 1px;
            }
            
            @keyframes formulaGlow {
                0% { opacity: 0.7; transform: scale(1); box-shadow: none; }
                50% { 
                    opacity: 1; 
                    transform: scale(1.02); 
                    box-shadow: 0 0 10px rgba(76, 175, 80, 0.4); /* зелёное свечение */
                }
                100% { opacity: 0.7; transform: scale(1); box-shadow: none; }
            }

            
            .formula-card {
                animation: formulaGlow 2.5s infinite;
                border: 1px solid #e0e0e0;
                background: rgba(0,0,0,0.02);
                border-radius: 3px;
                transition: box-shadow 0.3s ease;
            }

            
            .environment-scene {
                position: relative;
                height: 200px;
                background-image: url('/assets/bg-terryone.png');
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
                margin: 20px 0;
                border-radius: 3px;
                overflow: hidden;
                border: 1px solid #eee;
            }

            
            .animated-car {
                position: absolute;
                bottom: 15px;
                left: 0px;
                width: 100px;
                height: 100px;
                filter: drop-shadow(2px 4px 6px rgba(0,0,0,0.2));
                z-index: 10;
                transform: scale(0.8);
                transition: left 4s ease-in-out;
            }
            

            
            .metric-badge {
                transition: all 0.5s ease;
                opacity: 0;
                transform: translateY(20px);
                font-size: 1rem;
                padding: 6px 12px;
                font-weight: 500;
                letter-spacing: 0.5px;
                margin-right: 10px;
                border-radius: 2px;
            }
            
            .metric-visible-1 {
                opacity: 1;
                transform: translateY(0);
                transition-delay: 0s;
            }
            
            .metric-visible-2 {
                opacity: 1;
                transform: translateY(0);
                transition-delay: 0.3s;
            }
            
            .metric-visible-3 {
                opacity: 1;
                transform: translateY(0);
                transition-delay: 0.6s;
            }
            
            .card {
                border: 1px solid #eee;
                border-radius: 3px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                overflow: hidden;
                margin-bottom: 25px;
            }
            
            .card-header {
                background-color: #2e7d32;
                color: white;
                font-weight: 500;
                padding: 15px 20px;
                font-size: 0.9rem;
                letter-spacing: 0.5px;
                border: none;
                text-transform: uppercase;
            }
            
            .card-body {
                padding: 25px;
                background-color: white;
            }
            
            .btn-primary {
                background-color: #388e3c;
                border-color: #388e3c;
                font-weight: 500;
                padding: 10px 20px;
                border-radius: 2px;
                text-transform: uppercase;
                font-size: 0.85rem;
                letter-spacing: 0.5px;
                transition: all 0.3s ease;
            }
            
            .btn-primary:hover {
                background-color: #555;
                border-color: #555;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }
            
            .form-control, .input-group-text {
                border-radius: 2px;
                padding: 10px 15px;
                font-size: 0.9rem;
                border-color: #e0e0e0;
            }
            
            .input-group-text {
                background-color: #f8f9fa;
                font-weight: 500;
                color: #555;
            }
            
            .formula-text {
                font-weight: 500;
                color: #333;
                letter-spacing: 0.5px;
            }
            
            .error-message {
                color: #dc3545;
                font-size: 0.85rem;
                font-weight: 500;
                margin-top: 0.25rem;
                margin-bottom: 1rem;
                transition: opacity 0.3s ease;
            }
            
            .energy-badge {
                background-color: #2e7d32 !important;
            }
            
            .water-badge {
                background-color: #43a047 !important;
            }
            
            .co2-badge {
                background-color: #66bb6a !important;
            }
            
            .advantages-list li {
                margin-bottom: 12px;
                position: relative;
                padding-left: 25px;
                line-height: 1.5;
                font-size: 0.95rem;
                color: #444;
            }
            
            .advantages-list li:before {
                content: "✓";
                color: #555;
                font-weight: bold;
                position: absolute;
                left: 0;
                top: 0;
            }
            
            .terryOne-footer {
                background-color: #f8f8f8;
                padding: 0;
                margin-top: 50px;
                border-top: 1px solid #eee;
            }
            
            .footer-logo-bar {
                background-color: #2e7d32;
                padding: 15px 0;
                text-align: center;
            }
            
            .footer-logo {
                color: white;
                font-size: 1.6rem;
                font-weight: 700;
                letter-spacing: 1px;
                text-transform: lowercase;
            }
            
            .copyright {
                text-align: center;
                padding: 20px 0;
                font-size: 0.85rem;
                color: #777;
            }

            /* Вибрация */
            @keyframes shake {
            0% { transform: translateX(0); }
            25% { transform: translateX(-3px); }
            50% { transform: translateX(3px); }
            75% { transform: translateX(-3px); }
            100% { transform: translateX(0); }
            }

            .btn-primary {
            border-radius: 6px !important; /* закругление краёв */
            transition: all 0.3s ease;
            }

            .btn-primary.shake {
            animation: shake 0.3s ease;
            }

            @keyframes calmClick {
            0% { transform: scale(1); }
            30% { transform: scale(0.96); }
            60% { transform: scale(1.02); }
            100% { transform: scale(1); }
            }

            .btn-primary.calm-click {
            animation: calmClick 0.4s ease;
            }
            
            /* Стили для калькулятора полотенец */
            .towel-calculator {
                margin-top: 40px;
                background-color: white;
                padding: 30px 0;
                border-top: 1px solid #eee;
            }
            
            .towel-calculator h3 {
                text-align: center;
                margin-bottom: 30px;
                text-transform: uppercase;
                font-weight: 600;
                color: #333;
                font-size: 1.3rem;
                letter-spacing: 1px;
            }
            
            .towel-section {
                border-radius: 3px;
                margin-bottom: 20px;
                background-color: white;
            }
            
            .parameter-group {
                border-left: 3px solid #2e7d32;
                padding: 15px;
                margin-bottom: 20px;
                background-color: #fcfcfc;
                border-radius: 0 3px 3px 0;
            }
            
            .parameter-group h5 {
                font-weight: 600;
                color: #333;
                font-size: 1rem;
                margin-bottom: 15px;
                padding-bottom: 5px;
                border-bottom: 1px solid #eee;
            }
            
            .towel-table th {
                background-color: #f8f8f8;
                font-weight: 600;
                text-transform: uppercase;
                font-size: 0.85rem;
                letter-spacing: 0.5px;
                padding: 12px 15px;
                vertical-align: middle;
                color: #444;
            }
            
            .towel-table td {
                padding: 15px;
                vertical-align: middle;
                border-bottom: 1px solid #eee;
            }
            
            .towel-table-container {
                overflow-x: auto;
                margin-bottom: 20px;
                border: 1px solid #eee;
                border-radius: 3px;
            }
            
            .towel-type-cell {
                font-weight: 600;
                color: #333;
                text-transform: uppercase;
                font-size: 0.85rem;
                letter-spacing: 0.5px;
            }
            
            .cotton-color {
                color: #0066CC;
            }
            
            .hybrid-color {
                color: #2e7d32;
            }
            
            .saving-step {
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 20px;
                border-left: 4px solid #2e7d32;
                opacity: 0;
                transform: translateY(15px);
                transition: all 0.5s ease;
            }
            
            .saving-step.fade-in-delay-1 {
                transition-delay: 0.2s;
            }
            
            .saving-step.fade-in-delay-2 {
                transition-delay: 0.4s;
            }
            
            .saving-step.fade-in-delay-3 {
                transition-delay: 0.6s;
            }
            
            .savings-visualizer.active .saving-step {
                opacity: 1;
                transform: translateY(0);
            }
            
            .negative-bar {
                background-color: #ffebee !important;
                border-left: 3px solid #c62828 !important;
                box-shadow: inset 0 0 5px rgba(0,0,0,0.1);
                position: relative;
            }
            
            .negative-bar:before {
                content: "⚠️";
                position: absolute;
                right: 5px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 12px;
            }
            
            .progress-cost_increase {
                background-color: #c62828 !important;
            }
            
            .progress-washing {
                background-color: #00ACC1 !important;
            }
            
            .progress-initial_saving {
                background-color: #9C27B0 !important;
            }
            
            .current-total {
                font-weight: 600;
                color: #333;
                text-align: right;
                margin-top: 5px;
                white-space: nowrap;
            }
            
            .progress-bar-container {
                height: 30px;
                background-color: #f0f0f0;
                border-radius: 3px;
                overflow: hidden;
                margin-bottom: 10px;
                box-shadow: inset 0 1px 3px rgba(0,0,0,0.1);
            }
            
            .progress-energy {
                background-color: #FF6B00;
            }
            
            .progress-chemical {
                background-color: #0066CC;
            }
            
            .progress-equipment {
                background-color: #8B4513;
            }
            
            .progress-replacement {
                background-color: #00C853;
            }
            
            .progress-bar {
                height: 100%;
                color: white;
                text-align: right;
                padding: 0 15px;
                line-height: 30px;
                font-weight: 500;
                font-size: 0.9rem;
                width: 0;
                transition: width 1s ease-in-out;
            }
            
            .step-name {
                font-weight: 600;
                color: #333;
                font-size: 1.05rem;
                flex-grow: 1;
                margin-left: 10px;
            }
            
            .step-badge {
                display: inline-block;
                min-width: 32px;
                height: 32px;
                border-radius: 50%;
                background-color: #2e7d32;
                color: white;
                text-align: center;
                font-weight: bold;
                line-height: 32px;
                font-size: 14px;
            }
            
            .step-value {
                font-weight: 700;
                color: #2e7d32;
                font-size: 1.1rem;
            }
            
            .step-description {
                font-size: 0.9rem;
                color: #666;
                margin-top: 5px;
            }
            
            .final-summary {
                border-left: 4px solid #00C853;
                padding-left: 15px;
                margin-top: 30px;
                font-size: 1.1rem;
                color: #333;
                background-color: #fcfcfc;
                padding: 15px;
                border-radius: 0 3px 3px 0;
            }
            
            .laundry-type-radio .form-check {
                margin-right: 20px;
                cursor: pointer;
            }
            
            .laundry-type-radio .form-check-input {
                cursor: pointer;
            }
            
            .laundry-params-card {
                border-left: 4px solid #2e7d32;
                transition: all 0.3s ease;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .fade-in-animation {
                animation: fadeIn 0.5s ease forwards;
            }
            
            .temperature-slider .rc-slider-track {
                background-color: #2e7d32;
            }
            
            .temperature-slider .rc-slider-handle {
                border-color: #2e7d32;
            }
            
            .fade-in-delay-1 {
                opacity: 0;
                animation: fadeIn 0.5s ease forwards;
                animation-delay: 0.1s;
            }
            
            .fade-in-delay-2 {
                opacity: 0;
                animation: fadeIn 0.5s ease forwards;
                animation-delay: 0.2s;
            }
            
            .fade-in-delay-3 {
                opacity: 0;
                animation: fadeIn 0.5s ease forwards;
                animation-delay: 0.3s;
            }
            
            .fade-in-delay-4 {
                opacity: 0;
                animation: fadeIn 0.5s ease forwards;
                animation-delay: 0.4s;
            }
            
            .payback-days {
                font-size: 1.8rem;
                font-weight: 700;
                color: #2e7d32;
                text-align: center;
                margin: 20px 0;
            }
            
            .payback-recommendation {
                background-color: #f0f8e5;
                border-left: 4px solid #2e7d32;
                padding: 15px;
                border-radius: 0 3px 3px 0;
                margin-top: 20px;
                font-weight: 500;
            }
            
            .results-placeholder {
                text-align: center;
                padding: 50px 20px;
                color: #888;
                font-size: 1rem;
                font-style: italic;
                background-color: #f9f9f9;
                border: 1px dashed #ddd;
                border-radius: 3px;
                margin: 20px 0;
            }
            
            .results-placeholder i {
                display: block;
                font-size: 2rem;
                margin-bottom: 15px;
                color: #aaa;
            }
            
            .form-section-title {
                font-weight: 600;
                color: #333;
                font-size: 0.9rem;
                margin: 15px 0 10px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .form-group {
                margin-bottom: 15px;
                padding-bottom: 15px;
                border-bottom: 1px solid #f0f0f0;
            }
            
            .form-group:last-child {
                border-bottom: none;
                padding-bottom: 0;
            }
            
            .input-description {
                font-size: 0.8rem;
                color: #777;
                margin-top: 5px;
            }

            .savings-visualizer {
                opacity: 0;
                transition: opacity 0.5s ease;
            }
            
            .savings-visualizer.active {
                opacity: 1;
            }

            .savings-visualizer .step-description {
                color: #5a6268;
                font-size: 0.9rem;
                margin: 4px 0;
            }

            .savings-visualizer .current-total {
                font-size: 0.9rem;
                margin-top: 4px;
            }

            /* Стили для секции метрик ресурсов */
            .resource-metrics-section {
                margin-bottom: 24px;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 8px;
            }

            .resource-metrics-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 16px;
            }

            .resource-metric {
                padding: 12px;
                background-color: white;
                border-radius: 6px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                transition: transform 0.2s;
            }

            .resource-metric:hover {
                transform: translateY(-3px);
                box-shadow: 0 3px 6px rgba(0,0,0,0.1);
            }

            .resource-metric-title {
                font-weight: 600;
                margin-bottom: 8px;
                color: #2d3748;
            }

            /* Цвета для прогресс-баров метрик */
            .progress-bar.bg-info {
                background-color: #2196F3;
            }

            .progress-bar.bg-warning {
                background-color: #FF9800;
            }

            .progress-bar.bg-success {
                background-color: #4CAF50;
            }

            .progress-bar.bg-danger {
                background-color: #E91E63;
            }

            /* Медиа-запросы для адаптивности */
            @media (max-width: 768px) {
                .resource-metrics-grid {
                    grid-template-columns: 1fr;
                }
            }

        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# ========================
# Физические формулы
# ========================
class EcoFormulas:
    @staticmethod
    def energy_savings(rooms: int) -> float:
        """Энергосбережение (кВт·ч/год)
        Формула:
        E = 365 × P × η × (1 - e^(-t/τ))
        где:
        P = 2.5 кВт/комната
        η = 0.85 (КПД)
        t = 8 часов/день
        τ = 4 (постоянная времени)
        """
        return 365 * 2.5 * 0.85 * rooms * (1 - math.exp(-8/4))

    @staticmethod
    def water_savings(rooms: int) -> float:
        """Экономия воды (м³/год)
        Формула:
        W = N × d × (V₀ - V₁) × C
        где:
        N = 300 дней
        d = 2 стирки/день
        V₀ = 18 л (станд.), V₁ = 12 л (эко)
        C = 0.001 (конвертация в м³)
        """
        return rooms * 300 * 2 * (18 - 12) * 0.001

    @staticmethod
    def co2_reduction(rooms: int) -> float:
        """Сокращение CO₂ (тонн/год)
        Формула:
        CO₂ = E × 0.4 + W × 0.3
        где:
        0.4 кг/кВт·ч и 0.3 кг/м³
        """
        return (EcoFormulas.energy_savings(rooms)*0.4 +
                EcoFormulas.water_savings(rooms)*0.3) / 1000

# ========================
# Формулы для калькулятора полотенец
# ========================
class TowelCalculator:
    @staticmethod
    def cycles_per_year(rooms, occupancy, wash_interval):
        """Рассчитывает количество стирок в год"""
        return (rooms * (occupancy / 100) * 365) / int(wash_interval)
    
    @staticmethod
    def lifespan_years(cycles_to_wear, cycles_per_year):
        """Рассчитывает срок службы полотенец в годах"""
        return cycles_to_wear / cycles_per_year
    
    @staticmethod
    def calculate_own_laundry_costs(inputs):
        """Расчет затрат для своей прачечной"""
        # Усовершенствованная формула для расчета потребления энергии
        # Базируется на физической модели нагрева воды: E = m*c*∆T
        # где m - масса, c - теплоемкость, ∆T - разница температур
        # Нормализуем с учетом стоимости энергии

        # Базовые затраты на энергию для хлопка (зависит от нагрева от 20°C до температуры стирки)
        cotton_energy_base = inputs["energy_cost"] * ((inputs["cotton_temp"] - 20) / 80)
        
        # Затраты на энергию для гибрида с учетом более низкой температуры
        hybrid_energy_base = inputs["energy_cost"] * ((inputs["hybrid_temp"] - 20) / 80)
        
        # Применяем коэффициент экономии (дополнительный фактор экономии, помимо температуры)
        hybrid_energy = hybrid_energy_base * (1 - 0.1)  # дополнительная 10% экономия за счет технологии
        
        # Затраты на химию для гибрида с учетом экономии
        hybrid_chemical = inputs["chemical_cost"] * (1 - inputs["chemical_saving_percent"] / 100)
        
        # Расчет амортизации с учетом разной степени износа оборудования
        # Гибридные полотенца снижают износ оборудования из-за более низкой температуры и меньшего веса
        cotton_equipment_cost = inputs["equipment_cost"]
        # Амортизация для гибрида с учетом экономии (15-25% в зависимости от температуры)
        equipment_saving_percent = min(25, max(15, (inputs["cotton_temp"] - inputs["hybrid_temp"]) / 3))
        hybrid_equipment_cost = inputs["equipment_cost"] * (1 - equipment_saving_percent / 100)
        
        # Общие затраты за цикл
        cotton_cycle_cost = cotton_energy_base + inputs["chemical_cost"] + inputs["water_cost"] + cotton_equipment_cost
        hybrid_cycle_cost = hybrid_energy + hybrid_chemical + inputs["water_cost"] + hybrid_equipment_cost
        
        # Экономия за цикл
        cycle_saving = cotton_cycle_cost - hybrid_cycle_cost
        
        return {
            "cotton_energy_cost": cotton_energy_base,
            "hybrid_energy_cost": hybrid_energy,
            "cotton_chemical_cost": inputs["chemical_cost"],
            "hybrid_chemical_cost": hybrid_chemical,
            "cotton_equipment_cost": cotton_equipment_cost,
            "hybrid_equipment_cost": hybrid_equipment_cost,
            "equipment_saving_percent": equipment_saving_percent,
            "cotton_cycle_cost": cotton_cycle_cost,
            "hybrid_cycle_cost": hybrid_cycle_cost,
            "cycle_saving": cycle_saving
        }
    
    @staticmethod
    def calculate_remote_laundry_costs(inputs):
        """Расчет затрат для удаленной прачечной"""
        # Стоимость стирки за кг
        cotton_cost = inputs["remote_cost_kg"] * inputs["cotton_weight"]
        hybrid_cost = inputs["remote_cost_kg"] * inputs["hybrid_weight"]
        
        # Экономия за цикл (в данном случае может быть 0, если вес одинаковый)
        cycle_saving = cotton_cost - hybrid_cost
        
        return {
            "cotton_cycle_cost": cotton_cost,
            "hybrid_cycle_cost": hybrid_cost,
            "cycle_saving": cycle_saving
        }
    
    @staticmethod
    def calculate_replacement_savings(inputs, cycles_per_year):
        """Расчет экономии на замене полотенец"""
        # Срок службы
        cotton_lifespan = inputs["cotton_cycles"] / cycles_per_year
        hybrid_lifespan = inputs["hybrid_cycles"] / cycles_per_year
        
        # Количество полотенец на один номер (обычно стандартный комплект: 2-3 шт)
        towels_per_room = 3  # Можно вынести в параметры
        
        # Общее количество полотенец
        total_towels = inputs["hotel_rooms"] * towels_per_room
        
        # Коэффициент скидки при оптовой закупке (на больших объемах скидка больше)
        volume_discount = max(0, min(0.2, 0.05 + (inputs["hotel_rooms"] / 1000) * 0.15))
        
        # Учитываем оптовые скидки
        cotton_cost_discounted = inputs["cotton_cost"] * (1 - volume_discount)
        hybrid_cost_discounted = inputs["hybrid_cost"] * (1 - volume_discount)
        
        # Количество замен за срок службы гибрида
        # Избегаем деления на ноль
        if cotton_lifespan > 0:
            cotton_replacements = hybrid_lifespan / cotton_lifespan
        else:
            cotton_replacements = 1.0
        
        # Экономия на заменах (с учетом количества полотенец и скидок)
        # Важно: (cotton_replacements - 1) может быть отрицательным, если хлопок имеет больший срок службы
        replacement_saving = max(0, (cotton_replacements - 1)) * cotton_cost_discounted * total_towels
        
        return {
            "cotton_lifespan": cotton_lifespan,
            "hybrid_lifespan": hybrid_lifespan,
            "cotton_replacements": cotton_replacements,
            "replacement_saving": replacement_saving,
            "towels_per_room": towels_per_room,
            "total_towels": total_towels,
            "volume_discount": volume_discount
        }
    
    @staticmethod
    def calculate_payback(inputs):
        """Основной метод расчета окупаемости"""
        # Расчет стирок в год
        cycles_per_year = TowelCalculator.cycles_per_year(
            inputs["hotel_rooms"], 
            inputs["hotel_occupancy"], 
            inputs["wash_interval"]
        )
        
        # Базовые расчеты
        total_towels = inputs["hotel_rooms"] * 3  # Стандартный комплект - 3 полотенца на номер
        
        # Вес хлопкового и гибридного полотенца (проверка на корректные значения)
        cotton_weight = inputs["cotton_weight"]  # кг
        hybrid_weight = inputs["hybrid_weight"]  # кг
        
        # Проверяем, что веса полотенец различаются
        if cotton_weight == hybrid_weight:
            # Корректируем вес гибридного полотенца, если он ошибочно задан равным хлопковому
            hybrid_weight = cotton_weight * 0.75  # Гибридное на 25% легче
        
        # Физические константы и коэффициенты для точных расчетов
        # Теплоемкость воды: 4.186 кДж/(кг·°C)
        water_heat_capacity = 4.186
        # КПД нагрева 80%
        heating_efficiency = 0.8
        # кВт·ч в кДж
        kwh_to_kj = 3600
        # Коэффициент экологичности производства электроэнергии: 0.5 кг CO2 на кВт·ч
        co2_per_kwh = 0.5
        # Вода на кг белья при стирке (в литрах)
        water_per_kg = 7
        
        # Стоимость ресурсов (если не указано в входных данных)
        energy_cost_per_kwh = inputs.get("energy_cost", 5)  # ₽/кВт·ч
        water_cost_per_liter = inputs.get("water_cost", 0.035) / 1000  # ₽/л (переводим из ₽/м³)
        
        # Температура стирки
        cotton_temp = inputs.get("cotton_temp", 60)  # °C
        hybrid_temp = inputs.get("hybrid_temp", 40)  # °C
        
        # РАСЧЕТ ЭКОНОМИИ РЕСУРСОВ
        
        # 1. Расчет экономии воды
        # Вода для стирки хлопковых полотенец (л/год)
        cotton_water = cycles_per_year * cotton_weight * water_per_kg
        # Вода для стирки гибридных полотенец (л/год)
        hybrid_water = cycles_per_year * hybrid_weight * water_per_kg
        # Экономия воды (л/год)
        water_saved = cotton_water - hybrid_water
        
        # 2. Расчет экономии энергии на нагрев
        # Энергия на нагрев для хлопка (кВт·ч/год)
        cotton_energy = (cycles_per_year * cotton_weight * water_per_kg * water_heat_capacity * (cotton_temp - 15)) / (kwh_to_kj * heating_efficiency)
        # Энергия на нагрев для гибрида (кВт·ч/год)
        hybrid_energy = (cycles_per_year * hybrid_weight * water_per_kg * water_heat_capacity * (hybrid_temp - 15)) / (kwh_to_kj * heating_efficiency)
        # Экономия энергии (кВт·ч/год)
        energy_saved = cotton_energy - hybrid_energy
        
        # 3. Расчет сокращения выбросов CO₂
        # CO₂ от производства электроэнергии для нагрева (кг/год)
        co2_saved = energy_saved * co2_per_kwh
        
        # Расчет затрат в зависимости от типа прачечной
        if inputs["laundry_type"] == "own":
            costs = TowelCalculator.calculate_own_laundry_costs(inputs)
        else:
            costs = TowelCalculator.calculate_remote_laundry_costs(inputs)
        
        # Экономия на цикле стирки в год
        annual_washing_saving = costs["cycle_saving"] * cycles_per_year
        
        # Корректировка: если годовая экономия слишком мала при значимой разнице в ресурсах,
        # добавляем прямой расчет экономии на ресурсах
        if abs(annual_washing_saving) < 10000 and (water_saved > 1000 or energy_saved > 1000):
            # Дополнительная экономия на воде (₽)
            water_saving = water_saved * water_cost_per_liter
            # Дополнительная экономия на электроэнергии (₽)
            energy_saving = energy_saved * energy_cost_per_kwh
            # Корректируем общую экономию на стирке
            annual_washing_saving = water_saving + energy_saving
        
        # РАСЧЕТ ЭКОНОМИИ НА ЗАМЕНЕ ПОЛОТЕНЕЦ
        
        # Срок службы в годах
        cotton_lifespan = inputs["cotton_cycles"] / (cycles_per_year / total_towels)
        hybrid_lifespan = inputs["hybrid_cycles"] / (cycles_per_year / total_towels)
        
        # Количество замен полотенец в год
        cotton_replacements_per_year = total_towels / cotton_lifespan if cotton_lifespan > 0 else 0
        hybrid_replacements_per_year = total_towels / hybrid_lifespan if hybrid_lifespan > 0 else 0
        
        # Количество сохраненных замен (сокращение замен)
        replacements_saved = cotton_replacements_per_year - hybrid_replacements_per_year
        
        # Коэффициент скидки при оптовой закупке
        volume_discount = max(0, min(0.2, 0.05 + (inputs["hotel_rooms"] / 1000) * 0.15))
        
        # Учитываем скидки при расчете стоимости полотенец
        cotton_cost_discounted = inputs["cotton_cost"] * (1 - volume_discount)
        hybrid_cost_discounted = inputs["hybrid_cost"] * (1 - volume_discount)
        
        # Расчет экономии на заменах (₽/год)
        replacement_saving = (cotton_cost_discounted * cotton_replacements_per_year) - (hybrid_cost_discounted * hybrid_replacements_per_year)
        
        # Годовая экономия на замене полотенец
        annual_replacement_saving = replacement_saving
        
        # Общая годовая экономия (₽/год)
        total_annual_saving = annual_washing_saving + annual_replacement_saving
        
        # Расчет дополнительных затрат при переходе с хлопка на гибрид (₽)
        additional_cost = (hybrid_cost_discounted - cotton_cost_discounted) * total_towels
        
        # Проверка, действительно ли гибрид дороже хлопка
        is_hybrid_more_expensive = additional_cost > 0
        
        # Срок окупаемости в днях
        if total_annual_saving > 0 and is_hybrid_more_expensive:
            payback_days = (additional_cost / total_annual_saving) * 365
        elif total_annual_saving > 0 and not is_hybrid_more_expensive:
            # Если гибрид дешевле хлопка, окупаемость мгновенная
            payback_days = 0
        else:
            # Экономия отрицательная или нулевая - окупаемость невозможна
            payback_days = float('inf')
        
        # Формирование шагов экономии для визуализации
        savings_steps = []
        
        # Сохраняем расчеты для дополнительных метрик
        additional_metrics = {
            "total_cycles": round(cycles_per_year),
            "water_saved": round(water_saved),
            "energy_saved": round(energy_saved),
            "co2_saved": round(co2_saved),
            "replacements_saved": round(replacements_saved),
            "water_saving_percent": min(round((water_saved / cotton_water) * 100), 40),
            "energy_saving_percent": min(round((energy_saved / cotton_energy) * 100), 50),
            "co2_saving_percent": min(round((co2_saved / (cotton_energy * co2_per_kwh)) * 100), 40),
            "replacements_saving_percent": min(round((replacements_saved / cotton_replacements_per_year) * 100) if cotton_replacements_per_year > 0 else 0, 50)
        }
        
        # Если гибрид изначально дешевле - добавляем эту информацию
        if not is_hybrid_more_expensive:
            price_diff = abs(additional_cost)
            savings_steps.append({
                "name": "Экономия на закупке",
                "value": round(price_diff),
                "desc": f"Гибридные полотенца дешевле хлопковых на {round(abs(hybrid_cost_discounted - cotton_cost_discounted))} ₽/комплект с учетом скидки {round(volume_discount*100)}%",
                "type": "initial_saving"
            })
        
        # Добавляем шаги экономии на ресурсах
        if inputs["laundry_type"] == "own":
            # Экономия на энергии для собственной прачечной
            energy_saving_amount = energy_saved * energy_cost_per_kwh
            if energy_saving_amount > 0:
                savings_steps.append({
                    "name": "Экономия на энергии",
                    "value": round(energy_saving_amount),
                    "desc": f"Снижение температуры стирки с {cotton_temp}°C до {hybrid_temp}°C и вес {cotton_weight} кг vs {hybrid_weight} кг",
                    "type": "energy"
                })
            
            # Экономия на воде для собственной прачечной
            water_saving_amount = water_saved * water_cost_per_liter
            if water_saving_amount > 0:
                savings_steps.append({
                    "name": "Экономия на воде",
                    "value": round(water_saving_amount),
                    "desc": f"Меньше воды из-за меньшего веса: {cotton_weight} кг vs {hybrid_weight} кг",
                    "type": "water"
                })
            
            # Экономия на химии
            chemical_saving = (costs["cotton_chemical_cost"] - costs["hybrid_chemical_cost"]) * cycles_per_year
            if chemical_saving > 0:
                savings_steps.append({
                    "name": "Экономия на химии",
                    "value": round(chemical_saving),
                    "desc": f"-{inputs['chemical_saving_percent']}% расход химикатов",
                    "type": "chemical"
                })
                
            # Экономия на амортизации оборудования
            if "cotton_equipment_cost" in costs and "hybrid_equipment_cost" in costs:
                equipment_saving = (costs["cotton_equipment_cost"] - costs["hybrid_equipment_cost"]) * cycles_per_year
                equipment_saving_percent = costs.get("equipment_saving_percent", 15)
                if equipment_saving > 0:
                    savings_steps.append({
                        "name": "Экономия на амортизации",
                        "value": round(equipment_saving),
                        "desc": f"Снижение износа оборудования на {round(equipment_saving_percent)}% из-за более низкой температуры",
                        "type": "equipment"
                    })
        elif costs["cycle_saving"] > 0:
            # Общая экономия на стирке для удаленной прачечной
            savings_steps.append({
                "name": "Экономия на стирке",
                "value": round(annual_washing_saving),
                "desc": f"Разница в весе комплектов: {inputs['cotton_weight']} кг vs {inputs['hybrid_weight']} кг",
                "type": "washing"
            })
        elif costs["cycle_saving"] < 0:
            # Если экономия отрицательная - отображаем как дополнительные затраты
            washing_cost_increase = abs(annual_washing_saving)
            if washing_cost_increase > 0:
                savings_steps.append({
                    "name": "Увеличение затрат на стирку",
                    "value": -round(washing_cost_increase),  # Отрицательное значение для отображения
                    "desc": f"Стирка гибрида дороже на {round(abs(costs['cycle_saving']), 2)} ₽/цикл",
                    "type": "cost_increase"
                })
        
        # Экономия на замене полотенец
        if replacement_saving > 0:
            savings_steps.append({
                "name": "Сокращение замен",
                "value": round(replacement_saving),
                "desc": f"В {round(hybrid_lifespan/cotton_lifespan, 1)} раза дольше срок службы ({round(replacements_saved)} замен в год)",
                "type": "replacement"
            })
        
        # Добавляем накопительные суммы для визуализации
        cumulative_sum = 0
        for step in savings_steps:
            step_value = step["value"]
            cumulative_sum += step_value
            step["cumulative"] = cumulative_sum
            
            # Если после шага с отрицательной экономией общая сумма стала положительной
            # добавляем информацию о компенсации затрат
            if step["type"] == "replacement" and "cost_increase" in [s["type"] for s in savings_steps] and cumulative_sum > 0:
                step["desc"] += ". Компенсирует увеличение затрат на стирку!"
        
        return {
            "payback_days": round(payback_days) if not math.isinf(payback_days) else -1,  # -1 как индикатор бесконечности
            "annual_saving": round(total_annual_saving),
            "washing_saving": round(annual_washing_saving),
            "replacement_saving": round(annual_replacement_saving),
            "additional_cost": round(additional_cost),
            "savings_steps": savings_steps,
            "hybrid_lifespan": round(hybrid_lifespan, 2),
            "cotton_lifespan": round(cotton_lifespan, 2),
            "cycles_per_year": round(cycles_per_year),
            "total_saving": cumulative_sum,
            "is_profitable": total_annual_saving > 0,
            "is_hybrid_more_expensive": is_hybrid_more_expensive,
            "has_negative_washing_saving": costs["cycle_saving"] < 0,
            "metrics": additional_metrics  # Добавляем расчеты дополнительных метрик для визуализации
        }

# ========================
# Анимированный интерфейс (стиль TerryOne)
# ========================
app.layout = html.Div([
    dcc.Store(id='animation-trigger'),
    dcc.Store(id='towel-calculation-results'),
    dcc.Store(id='savings-steps'),
    dcc.Store(id='savings-animation-trigger'),
    dcc.Store(id='calculation-complete'),
    
    # TerryOne шапка в стиле официального сайта
    html.Div([
        html.Div([
            html.H1([
                html.Span("terry", style={
                    "color": "#222", 
                    "fontWeight": "700", 
                    "fontSize": "2.4rem", 
                    "letterSpacing": "1px"
                }),
                html.Span("One", style={
                    "color": "#69f542",  # ярко-зелёный цвет, как на логотипе
                    "fontWeight": "700", 
                    "fontSize": "2.4rem",
                    "textTransform": "none"
                }),
                html.Span("™", style={
                    "color": "#222", 
                    "fontWeight": "700", 
                    "fontSize": "1.2rem", 
                    "marginLeft": "4px",
                    "verticalAlign": "super"
                })
            ], className="terryOne-logo"),
            html.Div([
                html.Span("СОВЕРШЕННЫЙ", className="terryOne-tag"),
                html.Span("ТЕХНОЛОГИЧНЫЙ", className="terryOne-tag"),
                html.Span("ИЗНОСОУСТОЙЧИВЫЙ", className="terryOne-tag"),
                html.Span("РЕВОЛЮЦИОННЫЙ", className="terryOne-tag"),
                html.Span("ЭНЕРГОЭФФЕКТИВНЫЙ", className="terryOne-tag"),
            ], className="terryOne-tagline")
        ], className="terryOne-container")
    ], className="terryOne-header"),
    
    html.Div([
        html.H2("КАЛЬКУЛЯТОР ЭКОНОМИЧЕСКОЙ ЭФФЕКТИВНОСТИ", className="text-center"),
        
        dbc.Container([
            # Сцена с динамическими объектами
            html.Div([
                html.Img(id='car-top', src="/assets/car.svg", className="animated-car"),
            ], className="environment-scene"),
            
            # Панель управления
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("РАСЧЕТ ЭКОНОМИИ"),
                        dbc.CardBody([
                            html.Div([
                                html.P([
                                    "Энергия: ",
                                    html.Span("365 × P × η × (1 - e⁻ᵗ/τ)", 
                                            className="formula-text"),
                                ], className="formula-card p-3 mb-3"),
                                html.P([
                                    "Вода: ",
                                    html.Span("N × d × (V₀ - V₁) × C",
                                            className="formula-text"),
                                ], className="formula-card p-3 mb-3"),
                                dbc.InputGroup([
                                    dbc.InputGroupText("Количество комнат"),
                                    dbc.Input(id='rooms', type='number', value=200,
                                            min=10, max=1000)
                                ], className="mb-1"),
                                # Добавляем подсказку о допустимом диапазоне
                                html.Small("Допустимый диапазон: от 10 до 1000 комнат", 
                                        style={"color": "#777", "marginBottom": "10px", "display": "block"}),
                                # Сообщение об ошибке
                                html.Div(id='input-error', className="error-message", style={'opacity': '0'}),
                                dbc.Button("РАССЧИТАТЬ", id='calculate-btn', 
                                        color="primary", className="w-100 mt-3")
                            ]),
                            html.Div([
                                html.Img(id='car-bottom', src="/assets/car.svg", className="animated-car"),
                            ], className="environment-scene mt-4")
                        ])
                    ], className="shadow-sm")
                ], md=4),
                
                # Результаты
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("ДИНАМИКА ПОКАЗАТЕЛЕЙ"),
                        dbc.CardBody([
                            dcc.Graph(id='live-graph'),
                            html.Div([
                                dbc.Badge(id='energy-badge',
                                        className="metric-badge me-2 energy-badge"),
                                dbc.Badge(id='water-badge',
                                        className="metric-badge me-2 water-badge"),
                                dbc.Badge(id='co2-badge',
                                        className="metric-badge co2-badge")
                            ], className="mt-4 text-center")
                        ])
                    ], className="shadow-sm")
                ], md=8)
            ], className="g-4 mt-3"),
            
            # Информационная панель
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("ПРЕИМУЩЕСТВА РЕШЕНИЙ TERRYONE"),
                        dbc.CardBody([
                            html.Ul([
                                html.Li("Экстремальная износоустойчивость и прочность - до 300 циклов стирки"),
                                html.Li("Высыхание на 50% быстрее благодаря якорной конструкции"),
                                html.Li("Экономия воды при стирке до 15% по сравнению с обычными решениями"),
                                html.Li("Устойчивые и минимальные усадки благодаря современным технологиям"),
                                html.Li("Самоокупаемость: экономия ресурсов компенсирует ваши затраты")
                            ], className="advantages-list")
                        ])
                    ], className="shadow-sm mt-4")
                ], md=12)
            ])
        ], fluid=True, className="terryOne-container"),
        
        # Калькулятор для сравнения полотенец
        dbc.Container([
            html.Div([
                html.H3("КАЛЬКУЛЯТОР СРАВНЕНИЯ ПОЛОТЕНЕЦ"),
                
                # Основной интерфейс калькулятора
                dbc.Row([
                    # Левая колонка - входные параметры
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("ПАРАМЕТРЫ РАСЧЕТА"),
                            dbc.CardBody([
                                # 1. Тип прачечной
                                html.Div(className="parameter-group", children=[
                                    html.H5("Тип прачечной"),
                                    dbc.RadioItems(
                                        id="laundry-type",
                                        options=[
                                            {"label": "Своя", "value": "own"},
                                            {"label": "Удалённая", "value": "remote"},
                                        ],
                                        value="own",
                                        inline=True,
                                        className="laundry-type-radio mb-2"
                                    ),
                                ]),
                                
                                # 2. Параметры своей прачечной
                                html.Div(id="own-laundry-params", className="parameter-group", children=[
                                    html.H5("Параметры своей прачечной"),
                                    
                                    # Группа параметров стоимости
                                    html.Div(className="form-group", children=[
                                        html.Div(className="form-section-title", children="Стоимость ресурсов"),
                                        
                                        # Здесь новая структура для полей ввода - заголовок как label внутри блока
                                        dbc.Row([
                                            dbc.Col([
                                                html.Label("Электроэнергия", htmlFor="energy-cost", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="energy-cost", type="text", value="7.5", debounce=True),
                                                    dbc.InputGroupText("₽/кВт·ч"),
                                                ]),
                                            ], className="mb-3"),
                                            
                                            dbc.Col([
                                                html.Label("Вода", htmlFor="water-cost", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="water-cost", type="text", value="45.0", debounce=True),
                                                    dbc.InputGroupText("₽/литр"),
                                                ]),
                                            ], className="mb-3"),
                                        ]),
                                        
                                        dbc.Row([
                                            dbc.Col([
                                                html.Label("Химия", htmlFor="chemical-cost", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="chemical-cost", type="text", value="18.0", debounce=True),
                                                    dbc.InputGroupText("₽/цикл"),
                                                ]),
                                            ], className="mb-3"),
                                            
                                            dbc.Col([
                                                html.Label("Амортизация", htmlFor="equipment-cost", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="equipment-cost", type="text", value="10.0", debounce=True),
                                                    dbc.InputGroupText("₽/цикл"),
                                                ]),
                                            ], className="mb-3"),
                                        ]),
                                    ]),
                                    
                                    # Группа параметров стирки
                                    html.Div(className="form-group", children=[
                                        html.Div(className="form-section-title", children="Параметры стирки"),
                                        
                                        # Структура для температур стирки
                                        dbc.Row([
                                            dbc.Col([
                                                html.Label("Температура (хлопок)", htmlFor="cotton-temp", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="cotton-temp", type="text", value="95", debounce=True),
                                                    dbc.InputGroupText("°C"),
                                                ]),
                                            ], className="mb-3"),
                                            
                                            dbc.Col([
                                                html.Label("Температура (гибрид)", htmlFor="hybrid-temp", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="hybrid-temp", type="text", value="35", debounce=True),
                                                    dbc.InputGroupText("°C"),
                                                ]),
                                            ], className="mb-3"),
                                        ]),
                                        
                                        # Экономия энергии и химии
                                        dbc.Row([
                                            dbc.Col([
                                                html.Label("Экономия энергии", htmlFor="energy-saving-percent", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="energy-saving-percent", type="text", value="33", disabled=True),
                                                    dbc.InputGroupText("%"),
                                                ]),
                                                html.Div("Рассчитывается на основе разницы температур", className="form-text text-muted mt-1"),
                                            ], className="mb-3"),
                                            
                                            dbc.Col([
                                                html.Label("Экономия химии", htmlFor="chemical-saving-percent", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="chemical-saving-percent", type="text", value="30", debounce=True),
                                                    dbc.InputGroupText("%"),
                                                ]),
                                                html.Div("Автоматически рассчитывается, но вы можете изменить значение", className="form-text text-muted mt-1"),
                                            ], className="mb-3"),
                                        ]),
                                    ]),
                                ]),
                                
                                # 3. Параметры удалённой прачечной
                                html.Div(id="remote-laundry-params", className="parameter-group", style={"display": "none"}, children=[
                                    html.H5("Параметры удалённой прачечной"),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Label("Стоимость стирки", htmlFor="remote-cost-kg", className="form-label"),
                                            dbc.InputGroup([
                                                dbc.Input(id="remote-cost-kg", type="text", value="70.0", debounce=True),
                                                dbc.InputGroupText("₽/кг"),
                                            ]),
                                        ], className="mb-3"),
                                    ]),
                                ]),
                                
                                # 4. Параметры отеля
                                html.Div(className="parameter-group", children=[
                                    html.H5("Параметры отеля"),
                                    dbc.Row([
                                        dbc.Col([
                                            html.Label("Количество номеров", htmlFor="hotel-rooms", className="form-label"),
                                            dbc.Input(id="hotel-rooms", type="text", value="150", debounce=True),
                                        ], className="mb-3"),
                                        
                                        dbc.Col([
                                            html.Label("Заполняемость", htmlFor="hotel-occupancy", className="form-label"),
                                            dbc.InputGroup([
                                                dbc.Input(id="hotel-occupancy", type="text", value="85", debounce=True),
                                                dbc.InputGroupText("%"),
                                            ]),
                                        ], className="mb-3"),
                                    ]),
                                    
                                    dbc.Row([
                                        dbc.Col([
                                            html.Label("Интервал стирки", htmlFor="wash-interval", className="form-label"),
                                            dbc.Select(
                                                id="wash-interval",
                                                options=[
                                                    {"label": "Ежедневно", "value": "1"},
                                                    {"label": "Каждые 2 дня", "value": "2"},
                                                    {"label": "Каждые 3 дня", "value": "3"},
                                                    {"label": "Каждые 4 дня", "value": "4"},
                                                ],
                                                value="1",
                                            ),
                                        ], className="mb-3"),
                                    ]),
                                ]),
                            ])
                        ], className="shadow-sm mb-4"),
                        
                        # Таблица параметров полотенец
                        dbc.Card([
                            dbc.CardHeader("ПАРАМЕТРЫ ПОЛОТЕНЕЦ"),
                            dbc.CardBody([
                                html.Div([
                                    html.Table([
                                        html.Thead([
                                            html.Tr([
                                                html.Th("Параметр"),
                                                html.Th("Хлопок", className="text-center cotton-color"),
                                                html.Th("Гибрид TerryOne", className="text-center hybrid-color"),
                                            ])
                                        ]),
                                        html.Tbody([
                                            html.Tr([
                                                html.Td("Стоимость комплекта (₽)"),
                                                html.Td([
                                                    dbc.Input(id="cotton-cost", type="text", value="1200", debounce=True)
                                                ], className="p-2"),
                                                html.Td([
                                                    dbc.Input(id="hybrid-cost", type="text", value="1800", debounce=True)
                                                ], className="p-2"),
                                            ]),
                                            html.Tr([
                                                html.Td("Вес комплекта (кг)"),
                                                html.Td([
                                                    dbc.Input(id="cotton-weight", type="text", value="1.8", debounce=True)
                                                ], className="p-2"),
                                                html.Td([
                                                    dbc.Input(id="hybrid-weight", type="text", value="0.9", debounce=True)
                                                ], className="p-2"),
                                            ]),
                                            html.Tr([
                                                html.Td("Стирок до износа"),
                                                html.Td([
                                                    dbc.Input(id="cotton-cycles", type="text", value="80", debounce=True)
                                                ], className="p-2"),
                                                html.Td([
                                                    dbc.Input(id="hybrid-cycles", type="text", value="300", debounce=True)
                                                ], className="p-2"),
                                            ]),
                                        ])
                                    ], className="table towel-table w-100")
                                ], className="towel-table-container"),
                                
                                dbc.Button(
                                    "РАССЧИТАТЬ ОКУПАЕМОСТЬ", 
                                    id="calculate-payback-btn",
                                    color="primary", 
                                    className="w-100 mt-3"
                                ),
                            ])
                        ], className="shadow-sm")
                    ], md=6),
                    
                    # Правая колонка - результаты
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("РЕЗУЛЬТАТЫ СРАВНЕНИЯ"),
                            dbc.CardBody([
                                # Заполнитель для первоначального отображения
                                html.Div(id="results-placeholder", className="results-placeholder", children=[
                                    html.I("📊", className="fas fa-chart-bar"),
                                    html.Div("Введите параметры и нажмите кнопку «Рассчитать окупаемость», чтобы увидеть результаты сравнения.", className=""),
                                ]),
                                
                                # Срок окупаемости
                                html.Div(id="results-container", style={"display": "none"}, children=[
                                    html.Div([
                                        html.H5("Срок окупаемости:", className="text-center mb-3"),
                                        html.Div(id="payback-days", className="payback-days"),
                                        html.Div(id="payback-recommendation", className="payback-recommendation", style={"display": "none"}),
                                    ], className="mb-4"),
                                    
                                    # Визуализация экономии
                                    html.Div([
                                        html.H5("Детализация экономии:", className="mb-3"),
                                        html.Div(id="savings-visualizer", className="savings-visualizer"),
                                        html.Div(id="final-summary", className="final-summary", style={"display": "none"}),
                                    ]),
                                ]),
                            ])
                        ], className="shadow-sm")
                    ], md=6),
                ]),
                
                # Дополнительная информация
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("ПОЯСНЕНИЯ К РАСЧЕТУ"),
                            dbc.CardBody([
                                html.P([
                                    html.Strong("Срок службы полотенец "),
                                    "(лет) = Стирок до износа / Стирок в год"
                                ]),
                                html.P([
                                    html.Strong("Стирок в год "),
                                    "= (365 / Интервал стирки) × Количество номеров × (Заполняемость / 100)"
                                ]),
                                html.P([
                                    html.Strong("Окупаемость "),
                                    "(дней) = (Дополнительные затраты / Годовая экономия) × 365"
                                ]),
                                html.P([
                                    "Где ",
                                    html.Strong("дополнительные затраты "),
                                    "= (Стоимость гибрида - Стоимость хлопка) × Количество номеров"
                                ]),
                            ])
                        ], className="shadow-sm mt-4")
                    ], md=12)
                ])
            ], className="towel-calculator")
        ], fluid=True, className="terryOne-container"),
        
        # Футер в стиле TerryOne
        html.Footer([
            # Черная полоса с лого
            html.Div([
            html.Span([
                html.Span("terry", style={"color": "#222", "fontWeight": "700"}),
                html.Span("O", style={"color": "#69f542", "fontWeight": "700", "textTransform": "none"}),
                html.Span("ne", style={"color": "#69f542", "fontWeight": "700"}),
                html.Sup("™", style={"color": "#222", "fontWeight": "700", "fontSize": "0.8rem", "marginLeft": "4px"})
            ], className="footer-logo")  # или .terryOne-logo в шапке


            ], className="footer-logo-bar"),
            # Копирайт
            html.Div([
                "© 2023 TerryOne - Революция в текстильной индустрии HORECA"
            ], className="copyright")
        ], className="terryOne-footer")
    ])
])

# Проверка валидности ввода
@app.callback(
    [Output('input-error', 'children'),
     Output('input-error', 'style'),
     Output('animation-trigger', 'data')],  # Добавляем триггер для анимации
    [Input('rooms', 'value'),
     Input('calculate-btn', 'n_clicks')]    # Отслеживаем нажатие кнопки
)
def validate_input(rooms, n_clicks):
    trigger = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    error_message = ""
    error_style = {'opacity': '0'}

    if rooms is None:
        error_message = "Пожалуйста, введите верное количество комнат"
        error_style = {'opacity': '1'}
    else:
        try:
            rooms_value = float(rooms)
            if rooms_value < 10:
                error_message = f"Минимальное количество комнат: 10 (введено: {rooms_value})"
                error_style = {'opacity': '1'}
            elif rooms_value > 1000:
                error_message = f"Максимальное количество комнат: 1000 (введено: {rooms_value})"
                error_style = {'opacity': '1'}
        except:
            error_message = "Введите числовое значение"
            error_style = {'opacity': '1'}

    # Только если ошибок нет — разрешаем анимацию
    if trigger == 'calculate-btn' and n_clicks and error_message == "":
        timestamp = int(time.time() * 1000)
        return "", {'opacity': '0'}, timestamp

    return error_message, error_style, no_update


# ========================
# Логика анимаций и расчетов
# ========================
@app.callback(
    Output('live-graph', 'figure'),
     Output('energy-badge', 'children'),
     Output('water-badge', 'children'),
     Output('co2-badge', 'children'),
     Output('energy-badge', 'className'),
     Output('water-badge', 'className'),
     Output('co2-badge', 'className'),
    [Input('calculate-btn', 'n_clicks'),
     Input('animation-trigger', 'data')],  # Добавляем триггер анимации как вход
    [State('rooms', 'value')]
)
def update_system(n_clicks, animation_trigger, rooms):
    if not n_clicks:
        return [no_update]*7
    
    ctx = dash.callback_context
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    is_animation_reset = triggered_id == 'animation-trigger'
   
    
    # Используем тот же подход к валидации, что и в функции validate_input
    try:
        rooms_value = float(rooms)
        if rooms_value < 10 or rooms_value > 1000:
            return [no_update]*7
    except:
        return [no_update]*7
        
    # Расчет показателей
    energy = EcoFormulas.energy_savings(rooms_value)
    water = EcoFormulas.water_savings(rooms_value)
    co2 = EcoFormulas.co2_reduction(rooms_value)
    
    # Генерация графика
    months = pd.date_range('2023-01', periods=12, freq='M')
    df = pd.DataFrame({
        'Месяц': months,
        'Энергия (кВт·ч)': [energy * (0.8 + 0.2*math.sin(i/2)) for i in range(12)],
        'Вода (м³)': [water * (0.9 - 0.1*math.cos(i/3)) for i in range(12)]
    })
    
    fig = px.line(df, x='Месяц', y=['Энергия (кВт·ч)', 'Вода (м³)'],
                 template='plotly_white',
                 line_shape='spline')
    
    # Применяем цвета TerryOne и добавляем всплывающие подсказки
    fig.update_traces(
        line=dict(color='#333', width=3),
        selector=dict(name='Энергия (кВт·ч)'),
        hovertemplate='%{y:.0f} кВт·ч<br>Месяц: %{x|%B %Y}<extra></extra>'
    )
    fig.update_traces(
        line=dict(color='#777', width=3),
        selector=dict(name='Вода (м³)'),
        hovertemplate='%{y:.1f} м³<br>Месяц: %{x|%B %Y}<extra></extra>'
    )

    
    
    # Улучшаем внешний вид графика
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Montserrat"
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#333",
            borderwidth=1
        ),
        margin=dict(t=50, l=50, r=20, b=50)
    )
    
    # Анимация машины
    car_speed = 5/(rooms_value/200)  # Базовая формула
    # Ограничиваем значение
    car_speed = max(2, min(8, car_speed))
    # Убираем box-shadow и задаем анимацию
    car_animation = {
        'left': '100%', 
        'transition': f'left {car_speed}s ease-in-out',
        'transform': 'scale(0.8)'
    }


    return (
        fig,
        f"⚡ {energy:.0f} кВт·ч",
        f"💧 {water:.0f} м³",
        f"🌿 {co2:.1f} т CO₂",
        "metric-badge metric-visible-1 energy-badge",
        "metric-badge metric-visible-2 water-badge",
        "metric-badge metric-visible-3 co2-badge",
    )

# ========================
# Колбэки для калькулятора полотенец
# ========================

# Переключение типа прачечной
@app.callback(
    [Output("own-laundry-params", "style"),
     Output("remote-laundry-params", "style")],
    [Input("laundry-type", "value")]
)
def toggle_laundry_type(laundry_type):
    if laundry_type == "own":
        return {"display": "block"}, {"display": "none"}
    else:
        return {"display": "none"}, {"display": "block"}

# Автоматический расчет процента экономии энергии на основе разницы температур
@app.callback(
    Output("energy-saving-percent", "value"),
    [Input("cotton-temp", "value"),
     Input("hybrid-temp", "value")]
)
def calculate_energy_saving(cotton_temp, hybrid_temp):
    try:
        cotton_temp = float(cotton_temp.replace(',', '.')) if cotton_temp else 0
        hybrid_temp = float(hybrid_temp.replace(',', '.')) if hybrid_temp else 0
        
        if cotton_temp and hybrid_temp and cotton_temp > hybrid_temp:
            # Примерная формула: чем больше разница, тем больше экономия
            saving = round((cotton_temp - hybrid_temp) / cotton_temp * 100 * 0.9)  # 90% от пропорциональной разницы
            return str(saving)
        return "0"
    except:
        return "0"

# Новый колбэк для автоматического расчета экономии химии
@app.callback(
    Output("chemical-saving-percent", "value"),
    [Input("cotton-temp", "value"),
     Input("hybrid-temp", "value")]
)
def update_chemical_saving(cotton_temp, hybrid_temp):
    return str(calculate_chemical_saving(cotton_temp, hybrid_temp))

def calculate_chemical_saving(cotton_temp, hybrid_temp):
    try:
        cotton_temp = float(cotton_temp.replace(',', '.')) if cotton_temp else 0
        hybrid_temp = float(hybrid_temp.replace(',', '.')) if hybrid_temp else 0
        
        if cotton_temp and hybrid_temp and cotton_temp > hybrid_temp:
            # Формула: при снижении температуры на ~40% снижается расход химии на ~30%
            saving = round((cotton_temp - hybrid_temp) / cotton_temp * 100 * 0.75)  # 75% от пропорции
            return saving
        return 0
    except:
        return 0

# Расчет окупаемости полотенец
@app.callback(
    [Output("towel-calculation-results", "data"),
     Output("savings-steps", "data"),
     Output("savings-animation-trigger", "data")],
    [Input("calculate-payback-btn", "n_clicks")],
    [State("laundry-type", "value"),
     State("energy-cost", "value"),
     State("water-cost", "value"),
     State("chemical-cost", "value"),
     State("equipment-cost", "value"),
     State("cotton-temp", "value"),
     State("hybrid-temp", "value"),
     State("energy-saving-percent", "value"),
     State("chemical-saving-percent", "value"),
     State("remote-cost-kg", "value"),
     State("hotel-rooms", "value"),
     State("hotel-occupancy", "value"),
     State("wash-interval", "value"),
     State("cotton-cost", "value"),
     State("hybrid-cost", "value"),
     State("cotton-weight", "value"),
     State("hybrid-weight", "value"),
     State("cotton-cycles", "value"),
     State("hybrid-cycles", "value")]
)
def calculate_towel_payback(n_clicks, laundry_type, energy_cost, water_cost, chemical_cost, equipment_cost,
                           cotton_temp, hybrid_temp, energy_saving_percent, chemical_saving_percent,
                           remote_cost_kg, hotel_rooms, hotel_occupancy, wash_interval,
                           cotton_cost, hybrid_cost, cotton_weight, hybrid_weight,
                           cotton_cycles, hybrid_cycles):
    if not n_clicks:
        return no_update, no_update, no_update
    
    try:
        # Конвертируем текстовые значения в числа
        energy_cost = float(energy_cost.replace(',', '.')) if energy_cost else 0
        water_cost = float(water_cost.replace(',', '.')) if water_cost else 0
        chemical_cost = float(chemical_cost.replace(',', '.')) if chemical_cost else 0
        equipment_cost = float(equipment_cost.replace(',', '.')) if equipment_cost else 0
        cotton_temp = float(cotton_temp.replace(',', '.')) if cotton_temp else 0
        hybrid_temp = float(hybrid_temp.replace(',', '.')) if hybrid_temp else 0
        energy_saving_percent = float(energy_saving_percent.replace(',', '.')) if energy_saving_percent else 0
        chemical_saving_percent = float(chemical_saving_percent.replace(',', '.')) if chemical_saving_percent else 0
        remote_cost_kg = float(remote_cost_kg.replace(',', '.')) if remote_cost_kg else 0
        hotel_rooms = int(float(hotel_rooms.replace(',', '.'))) if hotel_rooms else 0
        hotel_occupancy = float(hotel_occupancy.replace(',', '.')) if hotel_occupancy else 0
        cotton_cost = float(cotton_cost.replace(',', '.')) if cotton_cost else 0
        hybrid_cost = float(hybrid_cost.replace(',', '.')) if hybrid_cost else 0
        cotton_weight = float(cotton_weight.replace(',', '.')) if cotton_weight else 0
        hybrid_weight = float(hybrid_weight.replace(',', '.')) if hybrid_weight else 0
        cotton_cycles = int(float(cotton_cycles.replace(',', '.'))) if cotton_cycles else 0
        hybrid_cycles = int(float(hybrid_cycles.replace(',', '.'))) if hybrid_cycles else 0
        
        # Проверка обязательных полей после конвертации
        if None in [hotel_rooms, hotel_occupancy, wash_interval, 
                    cotton_cost, hybrid_cost, cotton_weight, hybrid_weight,
                    cotton_cycles, hybrid_cycles]:
            return no_update, no_update, no_update
        
        if laundry_type == "own" and None in [energy_cost, water_cost, chemical_cost, equipment_cost,
                                            cotton_temp, hybrid_temp, energy_saving_percent, 
                                            chemical_saving_percent]:
            return no_update, no_update, no_update
        
        if laundry_type == "remote" and remote_cost_kg is None:
            return no_update, no_update, no_update
        
        # Создаем словарь входных параметров
        inputs = {
            "laundry_type": laundry_type,
            "energy_cost": energy_cost,
            "water_cost": water_cost,
            "chemical_cost": chemical_cost,
            "equipment_cost": equipment_cost,
            "cotton_temp": cotton_temp,
            "hybrid_temp": hybrid_temp,
            "energy_saving_percent": energy_saving_percent,
            "chemical_saving_percent": chemical_saving_percent,
            "remote_cost_kg": remote_cost_kg,
            "hotel_rooms": hotel_rooms,
            "hotel_occupancy": hotel_occupancy,
            "wash_interval": wash_interval,
            "cotton_cost": cotton_cost,
            "hybrid_cost": hybrid_cost,
            "cotton_weight": cotton_weight,
            "hybrid_weight": hybrid_weight,
            "cotton_cycles": cotton_cycles,
            "hybrid_cycles": hybrid_cycles
        }
        
        # Расчет окупаемости
        result = TowelCalculator.calculate_payback(inputs)
        
        # Триггер для анимации - текущее время
        timestamp = int(time.time() * 1000)
        
        return result, result["savings_steps"], timestamp
    except Exception as e:
        print(f"Ошибка при расчете окупаемости: {e}")
        return no_update, no_update, no_update

# Отображение результатов расчета
@app.callback(
    [Output("payback-days", "children"),
     Output("payback-recommendation", "children"),
     Output("payback-recommendation", "style"),
     Output("calculation-complete", "data")],
    [Input("towel-calculation-results", "data")]
)
def display_payback_results(results):
    if not results:
        return no_update, no_update, no_update, no_update
    
    payback_days = results["payback_days"]
    is_profitable = results.get("is_profitable", False)
    is_hybrid_more_expensive = results.get("is_hybrid_more_expensive", True)
    
    # Проверяем невозможность окупаемости (значение -1 - индикатор бесконечности)
    if payback_days == -1:
        # Случай, когда гибрид не приносит экономию
        recommendation = "Внедрение не рекомендуется. Экономия отрицательная или отсутствует."
        rec_style = {"display": "block", "background-color": "#ffebee", "color": "#c62828"}
        return "∞", recommendation, rec_style, {"complete": True}
    
    # Случай, когда гибрид дешевле хлопка и приносит экономию
    if not is_hybrid_more_expensive and is_profitable:
        recommendation = "Гибрид дешевле хлопка и приносит экономию! Рекомендуем немедленное внедрение! 🚀"
        rec_style = {"display": "block", "background-color": "#e8f5e9", "color": "#2e7d32"}
        return "0 дней", recommendation, rec_style, {"complete": True}
    
    # Обычные случаи с расчетом окупаемости
    if payback_days < 30:
        recommendation = f"Гибрид окупится менее чем за месяц ({payback_days} дней). Срочно внедряйте! 🚀"
        rec_style = {"display": "block", "background-color": "#e8f5e9", "color": "#2e7d32"}
    elif payback_days < 90:
        recommendation = f"Гибрид окупится за {payback_days} дней (менее 3 месяцев). Рекомендуем к внедрению! 👍"
        rec_style = {"display": "block", "background-color": "#f0f8e5", "color": "#33691e"}
    elif payback_days < 180:
        recommendation = f"Гибрид окупится за {payback_days} дней (менее полугода). Экономически обоснованно. ✓"
        rec_style = {"display": "block", "background-color": "#f9fbe7", "color": "#827717"}
    else:
        recommendation = f"Срок окупаемости: {payback_days} дней. Рассмотрите возможность внедрения в долгосрочной перспективе."
        rec_style = {"display": "block", "background-color": "#fff8e1", "color": "#ff6f00"}
    
    return f"{payback_days} дней", recommendation, rec_style, {"complete": True}

# Управление отображением контейнера результатов и заполнителя
@app.callback(
    [Output("results-container", "style"),
     Output("results-placeholder", "style")],
    [Input("calculation-complete", "data")]
)
def toggle_results_visibility(calculation_complete):
    if calculation_complete:
        return {"display": "block"}, {"display": "none"}
    return {"display": "none"}, {"display": "block"}

# Создание визуализации экономии
@app.callback(
    [Output("savings-visualizer", "children"),
     Output("savings-visualizer", "className"),
     Output("final-summary", "children"),
     Output("final-summary", "style")],
    [Input("savings-animation-trigger", "data"),
     Input("calculation-complete", "data")],
    [State("savings-steps", "data"),
     State("towel-calculation-results", "data")]
)
def create_savings_visualization(trigger, complete, steps, results):
    if not trigger or not complete or not steps or not results:
        return no_update, no_update, no_update, no_update
    
    # Получаем дополнительные метрики из результатов
    metrics = results.get("metrics", {})
    has_metrics = bool(metrics)
    
    # Если экономия отрицательная или нулевая и нет шагов экономии
    if not steps or len(steps) == 0:
        no_savings_html = html.Div([
            html.Div([
                html.Div([
                    html.Div("+", className="step-badge", style={"backgroundColor": "#c62828"}),
                    html.Div("Отсутствие экономии", className="step-name")
                ], className="step-title"),
                html.Div("0 ₽", className="step-value", style={"color": "#c62828"})
            ], className="step-header"),
            
            html.Div([
                html.Div("При данных параметрах экономия не достигается", className="step-description"),
            ], className="step-info mt-2")
        ], className="saving-step fade-in-delay-1", **{"data-type": "warning"})
        
        return [no_savings_html], "savings-visualizer active", "Нет экономии при заданных параметрах", {"display": "block", "color": "#c62828"}
    
    # Создаем секцию метрик экономии ресурсов
    resource_metrics_html = []
    
    if has_metrics:
        resource_metrics_html = html.Div([
            html.H5("Экономия ресурсов:", className="my-3"),
            html.Div([
                # Экономия воды
                html.Div([
                    html.Div("Экономия воды", className="resource-metric-title"),
                    html.Div([
                        html.Div(className="progress", style={"height": "12px"}, children=[
                            html.Div(className="progress-bar bg-info", 
                                     style={"width": f"{metrics.get('water_saving_percent', 0)}%"})
                        ]),
                        html.Div(f"{metrics.get('water_saved', 0):,} литров", className="mt-1")
                    ])
                ], className="resource-metric"),
                
                # Экономия энергии
                html.Div([
                    html.Div("Экономия энергии", className="resource-metric-title"),
                    html.Div([
                        html.Div(className="progress", style={"height": "12px"}, children=[
                            html.Div(className="progress-bar bg-warning", 
                                     style={"width": f"{metrics.get('energy_saving_percent', 0)}%"})
                        ]),
                        html.Div(f"{metrics.get('energy_saved', 0):,} кВт*ч", className="mt-1")
                    ])
                ], className="resource-metric"),
                
                # Сокращение выбросов CO₂
                html.Div([
                    html.Div("Сокращение CO₂", className="resource-metric-title"),
                    html.Div([
                        html.Div(className="progress", style={"height": "12px"}, children=[
                            html.Div(className="progress-bar bg-success", 
                                     style={"width": f"{metrics.get('co2_saving_percent', 0)}%"})
                        ]),
                        html.Div(f"{metrics.get('co2_saved', 0):,} кг", className="mt-1")
                    ])
                ], className="resource-metric"),
                
                # Уменьшение замен полотенец
                html.Div([
                    html.Div("Меньше замен", className="resource-metric-title"),
                    html.Div([
                        html.Div(className="progress", style={"height": "12px"}, children=[
                            html.Div(className="progress-bar bg-danger", 
                                     style={"width": f"{metrics.get('replacements_saving_percent', 0)}%"})
                        ]),
                        html.Div(f"{metrics.get('replacements_saved', 0):,} замен в год", className="mt-1")
                    ])
                ], className="resource-metric")
            ], className="resource-metrics-grid")
        ], className="resource-metrics-section")
    
    # Создаем шаги визуализации
    steps_html = []
    
    # Определяем общую сумму для расчета процентов (только положительные значения)
    total_saving = sum(step.get("value", 0) for step in steps if step.get("value", 0) > 0)
    
    # Определяем значения для бейджей и иконок
    step_numbers = {
        "energy": "1",
        "chemical": "2",
        "equipment": "3",  # Добавляем номер для экономии на амортизации
        "replacement": "4", # Сдвигаем номер для экономии на заменах
        "washing": "1",
        "cost_increase": "!",
        "initial_saving": "0"
    }
    
    step_icons = {
        "energy": "⚡",
        "chemical": "🧪",
        "equipment": "🔧",  # Иконка для амортизации
        "replacement": "♻️",
        "washing": "💧",
        "cost_increase": "⚠️",
        "initial_saving": "💰"
    }
    
    # Определяем цвета текста для типов экономии
    step_colors = {
        "energy": "#FF6B00",
        "chemical": "#0066CC",
        "equipment": "#8B4513",  # Коричневый цвет для амортизации
        "replacement": "#00C853",
        "washing": "#00ACC1",
        "cost_increase": "#c62828",
        "initial_saving": "#9C27B0"
    }
    
    # Создаем заголовок для денежной экономии
    steps_header = html.H5("Финансовая экономия:", className="my-3") if has_metrics else None
    
    for i, step in enumerate(steps):
        # Определяем тип шага
        step_type = step.get("type", "default")
        progress_class = f"progress-{step_type}"
        
        # Получаем номер и иконку для шага
        step_number = step_numbers.get(step_type, str(i+1))
        step_icon = step_icons.get(step_type, "💰")
        step_color = step_colors.get(step_type, "#2e7d32")
        
        # Значение шага может быть отрицательным для отображения увеличения затрат
        step_value = step.get("value", 0)
        is_negative = step_value < 0
        
        # Рассчитываем ширину прогресс-бара
        if is_negative:
            # Для отрицательных значений используем абсолютное значение
            # но с особым стилем и цветом
            width_percent = min(95, max(10, abs(step_value) / (total_saving or 1) * 100))
        else:
            # Для положительных значений - обычный расчет
            width_percent = max(5, (step_value / (total_saving or 1)) * 100) if total_saving > 0 else 0
        
        # Стиль для прогресс-бара
        progress_style = {
            "width": f"{width_percent}%",
            "backgroundColor": step_color if not is_negative else "#c62828"
        }
        
        # Текст для прогресс-бара
        value_text = f"{step_icon} {abs(step_value):,} ₽ {'(дополнительные затраты)' if is_negative else ''}"
        
        # Создаем HTML для шага с улучшенной структурой
        step_html = html.Div([
            # Заголовок шага с номером и значением
            html.Div([
                html.Div([
                    html.Div(step_number, className="step-badge", style={"backgroundColor": step_color}),
                    html.Div(step.get("name", "Экономия"), className="step-name")
                ], className="step-title"),
                html.Div(f"{'-' if is_negative else ''}{abs(step_value):,} ₽", 
                         className="step-value", 
                         style={"color": "#c62828" if is_negative else step_color})
            ], className="step-header"),
            
            # Прогресс-бар с текстом только снаружи
            html.Div([
                # Текст снаружи прогресс-бара
                html.Div(value_text, className="progress-bar-text"),
                
                # Сам прогресс-бар (без текста внутри)
                html.Div(
                    "", 
                    className=f"progress-bar {progress_class} {'' if not is_negative else 'negative-bar'}",
                    style=progress_style
                )
            ], className="progress-bar-container"),
            
            # Блок с описанием и информацией о накоплении
            html.Div([
                html.Div(step.get("desc", ""), className="step-description"),
                html.Div(f"Накоплено: {step.get('cumulative', 0):,} ₽", 
                         className="current-total", 
                         style={"color": "#c62828" if step.get('cumulative', 0) < 0 else step_color, 
                                "fontWeight": "700"})
            ], className="step-info mt-2")
        ], className=f"saving-step fade-in-delay-{i+1}", **{"data-type": step_type})
        
        steps_html.append(step_html)
    
    # Итоговая сводка с периодом экономии в наиболее подходящих единицах
    years = results.get("hybrid_lifespan", 0)
    days = int(years * 365)
    
    if days < 7:  # Меньше недели
        period_text = f"{days} дней"
    elif days < 30:  # Меньше месяца
        weeks = days // 7
        period_text = f"{weeks} {'неделю' if weeks == 1 else 'недели' if 2 <= weeks <= 4 else 'недель'}"
    elif days < 365:  # Меньше года
        months = days // 30
        period_text = f"{months} {'месяц' if months == 1 else 'месяца' if 2 <= months <= 4 else 'месяцев'}"
    else:  # Больше года
        period_text = f"{years:.1f} {'год' if 1 <= years < 2 else 'года' if 2 <= years < 5 else 'лет'}"
    
    # Информация о сроке службы
    cotton_lifespan = results.get("cotton_lifespan", 0)
    hybrid_lifespan = results.get("hybrid_lifespan", 0)
    washing_saving = results.get("washing_saving", 0)
    replacement_saving = results.get("replacement_saving", 0)
    total_annual_saving = results.get("annual_saving", 0)
    has_negative_washing = results.get("has_negative_washing_saving", False)
    
    # Формируем финальную сводку с дополнительными деталями
    if total_annual_saving > 0:
        if hybrid_lifespan > cotton_lifespan:
            lifespan_ratio = hybrid_lifespan/cotton_lifespan
            lifespan_comparison = f"Срок службы гибрида в {hybrid_lifespan/cotton_lifespan:.1f} раза больше ({hybrid_lifespan:.1f} против {cotton_lifespan:.1f} лет)"
        else:
            lifespan_comparison = f"Срок службы: гибрид - {hybrid_lifespan:.1f} лет, хлопок - {cotton_lifespan:.1f} лет"
        
        summary_html = [
            html.Div(f"Общая экономия за {period_text}: {total_saving:,} ₽ 🎉", className="mb-2"),
            html.Div(lifespan_comparison, className="mt-1", style={"fontSize": "0.9rem", "color": "#555"})
        ]
    else:
        summary_html = "Экономия не достигается при заданных параметрах"
    
    # Объединяем все компоненты в финальную визуализацию
    # Если есть метрики ресурсов, добавляем их перед шагами финансовой экономии
    final_visualization = []
    
    if has_metrics:
        final_visualization.append(resource_metrics_html)
        final_visualization.append(steps_header)
    
    final_visualization.extend(steps_html)
    
    return final_visualization, "savings-visualizer active", summary_html, {"display": "block"}

# ========================
# Запуск приложения
# ========================
if __name__ == '__main__':
    app.run_server(debug=True, port=8051) 

server = app.server