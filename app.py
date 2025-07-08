from flask import Flask, request, jsonify
import numpy as np
import os

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

    <form action="/calcular_ardl" method="get">
      <label>M1_real.L1 (valor positivo): <input type="number" step="any" name="m1_l1"></label><br>
      <label>ITCMR.L1 (valor positivo): <input type="number" step="any" name="itcmr_l1"></label><br>
      <label>GS10.L0: <input type="number" step="any" name="gs10_l0"></label><br>
      <label>VP.L0 (valor positivo): <input type="number" step="any" name="vp_l0"></label><br><br>
      <input type="submit" value="Calcular ARDL">
    </form>

    <br><hr><br>

    <form action="/calcular_ecm" method="get">
      <label>D_LN_VP: <input type="number" step="any" name="d_vp"></label><br>
      <label>ecm: <input type="number" step="any" name="ecm"></label><br><br>
      <input type="submit" value="Calcular ECM">
    </form>
    '''

@app.route('/calcular_ardl')
def calcular_ardl():
    try:
        # Obtener y validar entradas
        m1_l1 = float(request.args.get('m1_l1', 0))
        itcmr_l1 = float(request.args.get('itcmr_l1', 0))
        gs10_l0 = float(request.args.get('gs10_l0', 0))
        vp_l0 = float(request.args.get('vp_l0', 0))

        if m1_l1 <= 0 or itcmr_l1 <= 0 or vp_l0 <= 0:
            raise ValueError("Las variables en log deben ser mayores que cero.")

        # Aplicar logaritmos solo donde corresponde
        ln_m1 = np.log(m1_l1)
        ln_itcmr = np.log(itcmr_l1)
        ln_vp = np.log(vp_l0)

        resultado = (ARDL_COEF['const']
                     + ARDL_COEF['LN_M1_real.L1'] * ln_m1
                     + ARDL_COEF['LN_ITCMR.L1'] * ln_itcmr
                     + ARDL_COEF['GS10.L0'] * gs10_l0
                     + ARDL_COEF['LN_VP.L0'] * ln_vp)

        return jsonify({
            'modelo': 'ARDL',
            'resultado_estimado': round(resultado, 4)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/calcular_ecm')
def calcular_ecm():
    try:
        d_vp = float(request.args.get('d_vp', 0))
        ecm = float(request.args.get('ecm', 0))

        resultado = (ECM_COEF['D_LN_VP'] * d_vp
                     + ECM_COEF['ecm'] * ecm)

        return jsonify({
            'modelo': 'ECM',
            'resultado_estimado': round(resultado, 4)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
