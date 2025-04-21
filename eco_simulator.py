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
                color: #666;
                font-size: 0.9rem;
                flex-grow: 1;
                margin-right: 15px;
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
        # Базовые затраты на энергию для хлопка (зависит от температуры)
        cotton_energy_base = inputs["energy_cost"] * (inputs["cotton_temp"] / 100)
        # Затраты на энергию для гибрида с учетом экономии
        hybrid_energy = cotton_energy_base * (1 - inputs["energy_saving_percent"] / 100)
        
        # Затраты на химию для гибрида с учетом экономии
        hybrid_chemical = inputs["chemical_cost"] * (1 - inputs["chemical_saving_percent"] / 100)
        
        # Общие затраты за цикл
        cotton_cycle_cost = cotton_energy_base + inputs["chemical_cost"] + inputs["water_cost"] + inputs["equipment_cost"]
        hybrid_cycle_cost = hybrid_energy + hybrid_chemical + inputs["water_cost"] + inputs["equipment_cost"]
        
        # Экономия за цикл
        cycle_saving = cotton_cycle_cost - hybrid_cycle_cost
        
        return {
            "cotton_energy_cost": cotton_energy_base,
            "hybrid_energy_cost": hybrid_energy,
            "cotton_chemical_cost": inputs["chemical_cost"],
            "hybrid_chemical_cost": hybrid_chemical,
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
        
        # Количество замен за срок службы гибрида
        cotton_replacements = hybrid_lifespan / cotton_lifespan
        
        # Экономия на заменах
        replacement_saving = (cotton_replacements - 1) * inputs["cotton_cost"] * inputs["hotel_rooms"]
        
        return {
            "cotton_lifespan": cotton_lifespan,
            "hybrid_lifespan": hybrid_lifespan,
            "cotton_replacements": cotton_replacements,
            "replacement_saving": replacement_saving
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
        
        # Расчет затрат в зависимости от типа прачечной
        if inputs["laundry_type"] == "own":
            costs = TowelCalculator.calculate_own_laundry_costs(inputs)
        else:
            costs = TowelCalculator.calculate_remote_laundry_costs(inputs)
        
        # Экономия на цикле стирки в год
        annual_washing_saving = costs["cycle_saving"] * cycles_per_year
        
        # Расчет экономии на замене полотенец
        replacement = TowelCalculator.calculate_replacement_savings(inputs, cycles_per_year)
        
        # Экономия на замене полотенец в год
        annual_replacement_saving = replacement["replacement_saving"] / replacement["hybrid_lifespan"]
        
        # Общая годовая экономия
        total_annual_saving = annual_washing_saving + annual_replacement_saving
        
        # Дополнительные затраты на гибрид
        additional_cost = (inputs["hybrid_cost"] - inputs["cotton_cost"]) * inputs["hotel_rooms"]
        
        # Срок окупаемости в днях
        if total_annual_saving > 0:
            payback_days = (additional_cost / total_annual_saving) * 365
        else:
            payback_days = float('inf')
        
        # Формирование шагов экономии для визуализации
        savings_steps = []
        
        if inputs["laundry_type"] == "own" and costs["cycle_saving"] > 0:
            # Экономия на энергии
            energy_saving = (costs["cotton_energy_cost"] - costs["hybrid_energy_cost"]) * cycles_per_year
            if energy_saving > 0:
                savings_steps.append({
                    "name": "Экономия на энергии",
                    "value": round(energy_saving),
                    "desc": f"Снижение температуры стирки с {inputs['cotton_temp']}°C до {inputs['hybrid_temp']}°C",
                    "type": "energy"
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
        
        # Экономия на замене полотенец (для обоих типов прачечной)
        if replacement["replacement_saving"] > 0:
            savings_steps.append({
                "name": "Сокращение замен",
                "value": round(replacement["replacement_saving"]),
                "desc": f"В {round(replacement['cotton_replacements'], 1)} раза дольше срок службы",
                "type": "replacement"
            })
        
        # Добавляем накопительные суммы
        cumulative_sum = 0
        for step in savings_steps:
            cumulative_sum += step["value"]
            step["cumulative"] = cumulative_sum
        
        return {
            "payback_days": round(payback_days),
            "annual_saving": round(total_annual_saving),
            "additional_cost": round(additional_cost),
            "savings_steps": savings_steps,
            "hybrid_lifespan": round(replacement["hybrid_lifespan"], 2),
            "cotton_lifespan": round(replacement["cotton_lifespan"], 2),
            "cycles_per_year": round(cycles_per_year),
            "total_saving": cumulative_sum
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
        html.H2("КАЛЬКУЛЯТОР ЭКОНОМИЧЕСКОЙ ЭФФЕКТИВНОСТИ"),
        
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
                                                    dbc.Input(id="energy-cost", type="number", value=5.0, step=0.1),
                                                    dbc.InputGroupText("₽/кВт·ч"),
                                                ]),
                                            ], className="mb-3"),
                                            
                                            dbc.Col([
                                                html.Label("Вода", htmlFor="water-cost", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="water-cost", type="number", value=35.0, step=0.1),
                                                    dbc.InputGroupText("₽/литр"),
                                                ]),
                                            ], className="mb-3"),
                                        ]),
                                        
                                        dbc.Row([
                                            dbc.Col([
                                                html.Label("Химия", htmlFor="chemical-cost", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="chemical-cost", type="number", value=12.0, step=0.5),
                                                    dbc.InputGroupText("₽/цикл"),
                                                ]),
                                            ], className="mb-3"),
                                            
                                            dbc.Col([
                                                html.Label("Амортизация", htmlFor="equipment-cost", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="equipment-cost", type="number", value=8.0, step=0.5),
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
                                                    dbc.Input(id="cotton-temp", type="number", value=90, min=30, max=95),
                                                    dbc.InputGroupText("°C"),
                                                ]),
                                            ], className="mb-3"),
                                            
                                            dbc.Col([
                                                html.Label("Температура (гибрид)", htmlFor="hybrid-temp", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="hybrid-temp", type="number", value=50, min=30, max=95),
                                                    dbc.InputGroupText("°C"),
                                                ]),
                                            ], className="mb-3"),
                                        ]),
                                        
                                        # Экономия энергии и химии
                                        dbc.Row([
                                            dbc.Col([
                                                html.Label("Экономия энергии", htmlFor="energy-saving-percent", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="energy-saving-percent", type="number", value=33),
                                                    dbc.InputGroupText("%"),
                                                ]),
                                                html.Div("Рассчитывается на основе разницы температур", className="form-text text-muted mt-1"),
                                            ], className="mb-3"),
                                            
                                            dbc.Col([
                                                html.Label("Экономия химии", htmlFor="chemical-saving-percent", className="form-label"),
                                                dbc.InputGroup([
                                                    dbc.Input(id="chemical-saving-percent", type="number", value=30),
                                                    dbc.InputGroupText("%"),
                                                ]),
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
                                                dbc.Input(id="remote-cost-kg", type="number", value=50.0, step=1.0),
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
                                            dbc.Input(id="hotel-rooms", type="number", value=100, min=1),
                                        ], className="mb-3"),
                                        
                                        dbc.Col([
                                            html.Label("Заполняемость", htmlFor="hotel-occupancy", className="form-label"),
                                            dbc.InputGroup([
                                                dbc.Input(id="hotel-occupancy", type="number", value=80, min=1, max=100),
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
                                                value="2",
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
                                                    dbc.Input(id="cotton-cost", type="number", value=1500, min=1, step=100)
                                                ], className="p-2"),
                                                html.Td([
                                                    dbc.Input(id="hybrid-cost", type="number", value=3300, min=1, step=100)
                                                ], className="p-2"),
                                            ]),
                                            html.Tr([
                                                html.Td("Вес комплекта (кг)"),
                                                html.Td([
                                                    dbc.Input(id="cotton-weight", type="number", value=1.5, min=0.1, step=0.1)
                                                ], className="p-2"),
                                                html.Td([
                                                    dbc.Input(id="hybrid-weight", type="number", value=1.5, min=0.1, step=0.1)
                                                ], className="p-2"),
                                            ]),
                                            html.Tr([
                                                html.Td("Стирок до износа"),
                                                html.Td([
                                                    dbc.Input(id="cotton-cycles", type="number", value=100, min=1, step=10)
                                                ], className="p-2"),
                                                html.Td([
                                                    dbc.Input(id="hybrid-cycles", type="number", value=300, min=1, step=10)
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
    if cotton_temp and hybrid_temp and cotton_temp > hybrid_temp:
        # Примерная формула: чем больше разница, тем больше экономия
        saving = round((cotton_temp - hybrid_temp) / cotton_temp * 100 * 0.9)  # 90% от пропорциональной разницы
        return saving
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
    
    # Проверка обязательных полей
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
        "energy_cost": float(energy_cost) if energy_cost else 0,
        "water_cost": float(water_cost) if water_cost else 0,
        "chemical_cost": float(chemical_cost) if chemical_cost else 0,
        "equipment_cost": float(equipment_cost) if equipment_cost else 0,
        "cotton_temp": float(cotton_temp) if cotton_temp else 0,
        "hybrid_temp": float(hybrid_temp) if hybrid_temp else 0,
        "energy_saving_percent": float(energy_saving_percent) if energy_saving_percent else 0,
        "chemical_saving_percent": float(chemical_saving_percent) if chemical_saving_percent else 0,
        "remote_cost_kg": float(remote_cost_kg) if remote_cost_kg else 0,
        "hotel_rooms": int(hotel_rooms),
        "hotel_occupancy": float(hotel_occupancy),
        "wash_interval": wash_interval,
        "cotton_cost": float(cotton_cost),
        "hybrid_cost": float(hybrid_cost),
        "cotton_weight": float(cotton_weight),
        "hybrid_weight": float(hybrid_weight),
        "cotton_cycles": int(cotton_cycles),
        "hybrid_cycles": int(hybrid_cycles)
    }
    
    # Расчет окупаемости
    result = TowelCalculator.calculate_payback(inputs)
    
    # Триггер для анимации - текущее время
    timestamp = int(time.time() * 1000)
    
    return result, result["savings_steps"], timestamp

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
    
    # Формируем рекомендацию
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
    
    # Создаем шаги визуализации
    steps_html = []
    
    # Определяем общую сумму для расчета процентов
    total_saving = results["total_saving"]
    
    # Определяем значения для бейджей и иконок
    step_numbers = {
        "energy": "+2",
        "chemical": "+5",
        "replacement": "+3"
    }
    
    step_icons = {
        "energy": "⚡",
        "chemical": "🧪",
        "replacement": "♻️"
    }
    
    # Определяем цвета текста для типов экономии
    step_colors = {
        "energy": "#FF6B00",
        "chemical": "#0066CC",
        "replacement": "#00C853"
    }
    
    for i, step in enumerate(steps):
        # Определяем тип шага
        step_type = step["type"]
        progress_class = f"progress-{step_type}"
        
        # Получаем номер и иконку для шага
        step_number = step_numbers.get(step_type, "+")
        step_icon = step_icons.get(step_type, "💰")
        step_color = step_colors.get(step_type, "#2e7d32")
        
        # Рассчитываем ширину прогресс-бара пропорционально вкладу в общую сумму
        # Добавляем небольшой минимум в 5% для видимости, но сохраняем пропорции
        percent_of_total = (step["value"] / total_saving) * 100 if total_saving > 0 else 0
        width_percent = max(5, percent_of_total)
        
        # Текст для прогресс-бара (только иконка - текст будет только снаружи)
        value_text = f"{step_icon} {step['value']:,} ₽"
        
        # Создаем HTML для шага с улучшенной структурой
        step_html = html.Div([
            # Заголовок шага с номером и значением
            html.Div([
                html.Div([
                    html.Div(step_number, className="step-badge", style={"backgroundColor": step_color}),
                    html.Div(step["name"], className="step-name")
                ], className="step-title"),
                html.Div(f"{step['value']:,} ₽", className="step-value", style={"color": step_color})
            ], className="step-header"),
            
            # Прогресс-бар с текстом только снаружи
            html.Div([
                # Текст снаружи прогресс-бара
                html.Div(value_text, className="progress-bar-text"),
                
                # Сам прогресс-бар (без текста внутри)
                html.Div(
                    "", 
                    className=f"progress-bar {progress_class}",
                    style={"width": f"{width_percent}%"}
                )
            ], className="progress-bar-container"),
            
            # Блок с описанием и информацией о накоплении
            html.Div([
                html.Div(step["desc"], className="step-description"),
                html.Div(f"Накоплено: {step['cumulative']:,} ₽", className="current-total", 
                         style={"color": step_color, "fontWeight": "700"})
            ], className="step-info mt-2")
        ], className=f"saving-step fade-in-delay-{i+1}", **{"data-type": step_type})
        
        steps_html.append(step_html)
    
    # Итоговая сводка с периодом экономии в наиболее подходящих единицах
    years = results["hybrid_lifespan"]
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
    
    summary_html = f"Общая экономия за {period_text}: {total_saving:,} ₽ 🎉"
    
    return steps_html, "savings-visualizer active", summary_html, {"display": "block"}

# ========================
# Запуск приложения
# ========================
if __name__ == '__main__':
    app.run_server(debug=True, port=8051) 

server = app.server
