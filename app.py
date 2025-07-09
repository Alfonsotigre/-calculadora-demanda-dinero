
from flask import Flask, request, jsonify
import os
import math

app = Flask(__name__)

ARDL_COEF = {
    'const': 4.5626,
    'LN_M1_real.L1': 0.5439,
    'LN_M1_real.L2': 0.0572,
    'LN_M1_real.L3': 0.1715,
    'LN_ITCMR.L0': 0.0810,
    'LN_ITCMR.L1': -0.2593,
    'GS10.L0': -0.0318,
    'LN_VP.L0': -0.0505
}

ECM_COEF = {
    'D_LN_ITCMR': 0.1317,
    'D_GS10': 0.0021,
    'D_LN_VP': -0.0626,
    'ecm': -0.2374,
    'const': -0.0060
}

@app.route('/')
def index():
    return '''
    <h2>Calculadora de Demanda de Dinero - Modelos ARDL y ECM</h2>
    <form action="/calcular_ardl" method="get">
      <label>LN_M1_real.L1: <input type="number" step="any" name="m1_l1"></label><br>
      <label>LN_M1_real.L2: <input type="number" step="any" name="m1_l2"></label><br>
      <label>LN_M1_real.L3: <input type="number" step="any" name="m1_l3"></label><br>
      <label>LN_ITCMR.L0: <input type="number" step="any" name="itcmr_l0"></label><br>
      <label>LN_ITCMR.L1: <input type="number" step="any" name="itcmr_l1"></label><br>
      <label>GS10.L0: <input type="number" step="any" name="gs10_l0"></label><br>
      <label>LN_VP.L0: <input type="number" step="any" name="vp_l0"></label><br><br>
      <input type="submit" value="Calcular ARDL">
    </form>
    <hr>
    <form action="/calcular_ecm" method="get">
      <label>D_LN_ITCMR: <input type="number" step="any" name="d_itcmr"></label><br>
      <label>D_GS10: <input type="number" step="any" name="d_gs10"></label><br>
      <label>D_LN_VP: <input type="number" step="any" name="d_vp"></label><br>
      <label>ecm: <input type="number" step="any" name="ecm"></label><br><br>
      <input type="submit" value="Calcular ECM">
    </form>
    '''

@app.route('/calcular_ardl')
def calcular_ardl():
    try:
        x1 = float(request.args.get('m1_l1', 0))
        x2 = float(request.args.get('m1_l2', 0))
        x3 = float(request.args.get('m1_l3', 0))
        x4 = float(request.args.get('itcmr_l0', 0))
        x5 = float(request.args.get('itcmr_l1', 0))
        x6 = float(request.args.get('gs10_l0', 0))
        x7 = float(request.args.get('vp_l0', 0))

        resultado = (
            ARDL_COEF['const']
            + ARDL_COEF['LN_M1_real.L1'] * x1
            + ARDL_COEF['LN_M1_real.L2'] * x2
            + ARDL_COEF['LN_M1_real.L3'] * x3
            + ARDL_COEF['LN_ITCMR.L0'] * x4
            + ARDL_COEF['LN_ITCMR.L1'] * x5
            + ARDL_COEF['GS10.L0'] * x6
            + ARDL_COEF['LN_VP.L0'] * x7
        )

        en_pesos = math.exp(resultado)
        return jsonify({'modelo': 'ARDL', 'resultado_estimado': round(resultado, 4), 'valor_en_pesos': round(en_pesos, 2)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calcular_ecm')
def calcular_ecm():
    try:
        x1 = float(request.args.get('d_itcmr', 0))
        x2 = float(request.args.get('d_gs10', 0))
        x3 = float(request.args.get('d_vp', 0))
        x4 = float(request.args.get('ecm', 0))

        resultado = (
            ECM_COEF['const']
            + ECM_COEF['D_LN_ITCMR'] * x1
            + ECM_COEF['D_GS10'] * x2
            + ECM_COEF['D_LN_VP'] * x3
            + ECM_COEF['ecm'] * x4
        )

        return jsonify({'modelo': 'ECM', 'resultado_estimado': round(resultado, 4)})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
