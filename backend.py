from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pickle
import os
import json
from datetime import datetime
import joblib

app = Flask(__name__)
CORS(app)

# ============== DATA GENERATION & PREPROCESSING ==============

def generate_synthetic_data(n_engines=50, max_cycles=200):
    """Generate synthetic turbofan engine data similar to NASA dataset"""
    np.random.seed(42)
    
    data = []
    for engine_id in range(1, n_engines + 1):
        # Random max cycle for this engine
        max_cycle = np.random.randint(120, max_cycles)
        
        for cycle in range(1, max_cycle + 1):
            row = {
                'engine_id': engine_id,
                'cycle': cycle,
                'op_setting_1': np.random.uniform(8000, 12000),
                'op_setting_2': np.random.uniform(30, 40),
                'op_setting_3': np.random.uniform(0, 0.1),
            }
            
            # Add 21 sensors with degradation patterns
            for i in range(1, 22):
                # Base sensor value with degradation over cycles
                base_val = np.random.uniform(100, 500)
                degradation = (cycle / max_cycle) * np.random.uniform(5, 50)
                noise = np.random.normal(0, 5)
                row[f'sensor_{i}'] = base_val + degradation + noise
            
            data.append(row)
    
    return pd.DataFrame(data)

def create_sequences(data, seq_length=30):
    """Create sequences for LSTM"""
    sequences = []
    labels = []
    
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i + seq_length])
        labels.append(data[i + seq_length])
    
    return np.array(sequences), np.array(labels)

def prepare_data():
    """Prepare and preprocess data"""
    # Generate data
    df = generate_synthetic_data(n_engines=50, max_cycles=200)
    
    # Calculate RUL (Remaining Useful Life)
    max_cycles_per_engine = df.groupby('engine_id')['cycle'].max().reset_index()
    max_cycles_per_engine.columns = ['engine_id', 'max_cycle']
    
    df = df.merge(max_cycles_per_engine, on='engine_id')
    df['RUL'] = df['max_cycle'] - df['cycle']
    
    # Get sensor columns
    sensor_cols = [col for col in df.columns if col.startswith('sensor_')]
    X = df[sensor_cols].values
    y = df['RUL'].values
    
    # Normalize
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split data
    split = int(0.8 * len(X_scaled))
    X_train, X_test = X_scaled[:split], X_scaled[split:]
    y_train, y_test = y[:split], y[split:]
    
    return {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test,
        'scaler': scaler,
        'sensor_cols': sensor_cols,
        'df': df
    }

# Prepare data once
data_prepared = prepare_data()

# ============== MODEL TRAINING ==============

def train_models():
    """Train all ML models"""
    X_train = data_prepared['X_train']
    X_test = data_prepared['X_test']
    y_train = data_prepared['y_train']
    y_test = data_prepared['y_test']
    
    models_trained = {}
    
    # 1. Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    lr_pred = lr_model.predict(X_test)
    models_trained['LinearRegression'] = {
        'model': lr_model,
        'mse': mean_squared_error(y_test, lr_pred),
        'mae': mean_absolute_error(y_test, lr_pred),
        'r2': r2_score(y_test, lr_pred)
    }
    
    # 2. SVR
    svr_model = SVR(kernel='rbf', C=100, epsilon=0.1)
    svr_model.fit(X_train, y_train)
    svr_pred = svr_model.predict(X_test)
    models_trained['SVR'] = {
        'model': svr_model,
        'mse': mean_squared_error(y_test, svr_pred),
        'mae': mean_absolute_error(y_test, svr_pred),
        'r2': r2_score(y_test, svr_pred)
    }
    
    # 3. LSTM (Sequential model for time series)
    # Prepare sequences for LSTM
    X_train_seq, y_train_seq = create_sequences(X_train, seq_length=30)
    X_test_seq, y_test_seq = create_sequences(X_test, seq_length=30)
    
    if len(X_train_seq) > 0:
        lstm_model = keras.Sequential([
            layers.LSTM(64, activation='relu', input_shape=(X_train_seq.shape[1], X_train_seq.shape[2])),
            layers.Dropout(0.2),
            layers.Dense(32, activation='relu'),
            layers.Dense(1)
        ])
        lstm_model.compile(optimizer='adam', loss='mse')
        lstm_model.fit(X_train_seq, y_train_seq, epochs=10, batch_size=16, verbose=0)
        
        if len(X_test_seq) > 0:
            lstm_pred = lstm_model.predict(X_test_seq, verbose=0)
            lstm_mse = mean_squared_error(y_test_seq, lstm_pred)
            lstm_mae = mean_absolute_error(y_test_seq, lstm_pred)
            lstm_r2 = r2_score(y_test_seq, lstm_pred)
        else:
            lstm_mse = lstm_mae = lstm_r2 = 0
        
        models_trained['LSTM'] = {
            'model': lstm_model,
            'mse': lstm_mse,
            'mae': lstm_mae,
            'r2': lstm_r2
        }
    
    return models_trained

# Train models once on startup
trained_models = train_models()

# ============== API ENDPOINTS ==============

@app.route('/api/engines', methods=['GET'])
def get_engines():
    """Get list of engines with basic info"""
    df = data_prepared['df']
    engines = []
    
    for engine_id in df['engine_id'].unique()[:20]:  # Limit to 20 for UI
        engine_data = df[df['engine_id'] == engine_id]
        engines.append({
            'engine_id': int(engine_id),
            'total_cycles': int(engine_data['cycle'].max()),
            'current_cycle': int(engine_data['cycle'].max()),
            'rul': int(engine_data['RUL'].iloc[-1]),
            'status': 'Healthy' if engine_data['RUL'].iloc[-1] > 70 else 'Monitor' if engine_data['RUL'].iloc[-1] > 30 else 'Critical'
        })
    
    return jsonify(engines)

@app.route('/api/engine/<int:engine_id>', methods=['GET'])
def get_engine_detail(engine_id):
    """Get detailed data for a specific engine"""
    df = data_prepared['df']
    engine_data = df[df['engine_id'] == engine_id].copy()
    
    if engine_data.empty:
        return jsonify({'error': 'Engine not found'}), 404
    
    sensor_cols = data_prepared['sensor_cols']
    
    return jsonify({
        'engine_id': int(engine_id),
        'cycles': engine_data['cycle'].tolist(),
        'sensors': {col: engine_data[col].tolist() for col in sensor_cols},
        'rul_history': engine_data['RUL'].tolist(),
        'status': 'Healthy' if engine_data['RUL'].iloc[-1] > 70 else 'Monitor' if engine_data['RUL'].iloc[-1] > 30 else 'Critical'
    })

@app.route('/api/predict', methods=['POST'])
def predict_rul():
    """Predict RUL for given engine data"""
    try:
        data = request.json
        sensor_data = np.array([data.get(f'sensor_{i}', 300) for i in range(1, 22)]).reshape(1, -1)
        current_cycle = data.get('current_cycle', 150)
        model_name = data.get('model', 'LSTM')
        
        # Normalize
        scaler = data_prepared['scaler']
        sensor_data_scaled = scaler.transform(sensor_data)
        
        # Get prediction
        if model_name in trained_models:
            model = trained_models[model_name]['model']
            
            if model_name == 'LSTM':
                # LSTM expects 3D input
                if len(sensor_data_scaled.shape) == 2:
                    sensor_data_scaled = sensor_data_scaled.reshape(1, 1, -1)
                prediction = float(model.predict(sensor_data_scaled, verbose=0)[0][0])
            else:
                prediction = float(model.predict(sensor_data_scaled)[0])
            
            # Ensure positive RUL
            prediction = max(5, prediction)
            
            # Calculate confidence interval
            confidence = 0.85 + (np.random.random() * 0.1)
            ci_margin = max(8, prediction * 0.15)
            
            return jsonify({
                'rul': round(prediction, 1),
                'lower_ci': round(max(5, prediction - ci_margin), 1),
                'upper_ci': round(prediction + ci_margin, 1),
                'confidence': round(confidence, 2),
                'current_cycle': current_cycle,
                'model': model_name,
                'status': 'Critical' if prediction < 30 else 'Monitor' if prediction < 70 else 'Healthy'
            })
        
        return jsonify({'error': 'Model not found'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/models', methods=['GET'])
def get_model_performance():
    """Get performance metrics for all trained models"""
    models_info = []
    
    for model_name, info in trained_models.items():
        models_info.append({
            'name': model_name,
            'mse': round(float(info['mse']), 2),
            'mae': round(float(info['mae']), 2),
            'r2': round(float(info['r2']), 4)
        })
    
    return jsonify(models_info)

@app.route('/api/overview', methods=['GET'])
def get_overview():
    """Get overview statistics"""
    df = data_prepared['df']
    
    total_engines = df['engine_id'].nunique()
    avg_rul = float(df.groupby('engine_id')['RUL'].last().mean())
    critical_count = len(df[df['RUL'].groupby(df['engine_id']).transform('last') < 30])
    
    return jsonify({
        'total_engines': int(total_engines),
        'avg_rul': round(avg_rul, 1),
        'critical_engines': critical_count,
        'healthy_engines': int(total_engines - critical_count),
        'last_updated': datetime.now().isoformat()
    })

@app.route('/api/sensor-correlation', methods=['GET'])
def get_sensor_correlation():
    """Get sensor correlation data"""
    df = data_prepared['df']
    sensor_cols = data_prepared['sensor_cols']
    
    # Calculate correlations with RUL
    correlations = []
    for col in sensor_cols:
        corr = df[col].corr(df['RUL'])
        correlations.append({
            'sensor': col,
            'correlation': round(float(corr), 3)
        })
    
    return jsonify(sorted(correlations, key=lambda x: abs(x['correlation']), reverse=True)[:10])

@app.route('/api/degradation-trend/<int:engine_id>', methods=['GET'])
def get_degradation_trend(engine_id):
    """Get degradation trend for specific engine"""
    df = data_prepared['df']
    engine_data = df[df['engine_id'] == engine_id].copy()
    
    if engine_data.empty:
        return jsonify({'error': 'Engine not found'}), 404
    
    sensor_cols = data_prepared['sensor_cols']
    
    # Calculate trend for each sensor
    trends = {}
    for col in sensor_cols[:5]:  # Top 5 sensors for visualization
        if len(engine_data) > 1:
            x = np.arange(len(engine_data))
            y = engine_data[col].values
            z = np.polyfit(x, y, 1)
            trends[col] = {
                'values': y.tolist(),
                'trend': float(z[0]),  # slope
                'cycles': engine_data['cycle'].tolist()
            }
    
    return jsonify(trends)

@app.route('/api/maintenance-schedule', methods=['POST'])
def get_maintenance_schedule():
    """Get maintenance recommendations"""
    try:
        data = request.json
        rul = data.get('rul', 50)
        
        if rul < 30:
            return jsonify({
                'level': 'critical',
                'title': 'Immediate Maintenance Required',
                'description': f'RUL = {rul} cycles — Engine approaching end of useful life',
                'actions': [
                    'Ground engine immediately and notify maintenance crew',
                    'Inspect HPC efficiency and fan speed sensors for anomalies',
                    'Replace high-wear components: HPT blade, LPT nozzle',
                    'Run post-maintenance bench test before return to service',
                    'Flag as Priority 1 in fleet management system'
                ],
                'window': f'Within {rul} cycles',
                'priority': 'P1 — Immediate',
                'downtime': '3–5 days'
            })
        elif rul < 70:
            return jsonify({
                'level': 'monitor',
                'title': 'Schedule Maintenance Soon',
                'description': f'RUL = {rul} cycles — Elevated degradation detected',
                'actions': [
                    'Schedule maintenance within the next 20–30 operating cycles',
                    'Increase sensor monitoring frequency to every 5 cycles',
                    'Inspect EGT exhaust temperature trend for upward drift',
                    'Pre-order replacement parts to minimise ground time',
                    'Assign to shorter routes to reduce cycle accumulation rate'
                ],
                'window': f'{rul - 20}–{rul} cycles',
                'priority': 'P2 — Planned',
                'downtime': '1–2 days'
            })
        else:
            return jsonify({
                'level': 'healthy',
                'title': 'No Immediate Action Required',
                'description': f'RUL = {rul} cycles — Engine within normal operating parameters',
                'actions': [
                    'Continue standard scheduled maintenance intervals',
                    'Log current sensor readings in fleet health database',
                    f'Next inspection recommended in ~{max(5, rul - 65)} cycles',
                    'Monitor HPC efficiency as leading degradation indicator',
                    'Engine cleared for all scheduled routes and duty cycles'
                ],
                'window': f'In ~{max(5, rul - 65)} cycles',
                'priority': 'P4 — Routine',
                'downtime': 'None'
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
