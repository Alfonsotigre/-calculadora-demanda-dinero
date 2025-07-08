from flask import Flask, request, jsonify
import os
import math

app = Flask(__name__)

# === Coeficientes significativos del modelo ARDL (p < 0.05) ===
ARDL_COEF = {
    'const': 4.5626,
    'LN_M1_real.L1': 0.5439,
    'LN_ITCMR.L1': -0.2593,
    'GS10.L0': -0.0318,
    'LN_VP.L0': -0.0505
}

# === Coeficientes significativos del modelo ECM (p < 0.05) ===
ECM_COEF = {
    'D_LN_VP': -0.0626,
    'ecm': -0.2374
}

@app.route('/')
def index():
    return '''
    <h2>Calculadora de Demanda de Dinero - Modelos ARDL y ECM</h2>
    <p><strong>Importante:</strong> Ingresar valores originales (no transformados). El sistema aplicará logaritmo natural cuando sea necesario.</p>
    <form action="/calcular_ardl" method="get">
      <label>M1_real (t-1): <input type="number" step="any" name="m1_l1"></label><br>
      <label>ITCMR (t-1): <input type="number" step="any" name="itcmr_l1"></label><br>
      <label>GS10 (nivel actual): <input type="number" step="any" name="gs10_l0"></label><br>
      <label>VP (nivel actual): <input type="number" step="any" name="vp_l0"></label><br><br>
      <input type="submit" value="Calcular ARDL">
    </form>
    <hr>
    <form action="/calcular_ecm" method="get">
      <label>∆ln(VP): <input type="number" step="any" name="d_vp"></label><br>
      <label>Error de cointegración (ecm): <input type="number" step="any" name="ecm"></label><br><br>
      <input type="submit" value="Calcular ECM">
    </form>
    '''

@app.route('/calcular_ardl')
def calcular_ardl():
    try:
        # Se aplican logaritmos donde corresponde
        x1 = math.log(float(request.args.get('m1_l1', 1)))
        x2 = math.log(float(request.args.get('itcmr_l1', 1)))
        x3 = float(request.args.get('gs10_l0', 0))  # No se aplica log
        x4 = math.log(float(request.args.get('vp_l0', 1)))

        resultado = (ARDL_COEF['const']
                     + ARDL_COEF['LN_M1_real.L1'] * x1
                     + ARDL_COEF['LN_ITCMR.L1'] * x2
                     + ARDL_COEF['GS10.L0'] * x3
                     + ARDL_COEF['LN_VP.L0'] * x4)

        return jsonify({'modelo': 'ARDL', 'resultado_estimado': round(resultado, 4)})

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calcular_ecm')
def calcular_ecm():
    try:
        x1 = float(request.args.get('d_vp', 0))
        x2 = float(request.args.get('ecm', 0))

        resultado = ECM_COEF['D_LN_VP'] * x1 + ECM_COEF['ecm'] * x2

        return jsonify({'modelo': 'ECM', 'resultado_estimado': round(resultado, 4)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

