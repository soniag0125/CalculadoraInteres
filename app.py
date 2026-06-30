import math
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Calculadora de Interés",
    page_icon="💰",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #5f6368;
        font-size: 1.05rem;
        margin-bottom: 1.2rem;
    }
    .formula-box {
        background-color: #f6f8fa;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1rem;
        font-size: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">Calculadora de Interés Simple y Compuesto</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Aplicación básica desarrollada con Python y Streamlit para practicar formularios, métricas, tablas y gráficos.</div>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Parámetros")
    capital = st.number_input("Capital inicial", min_value=0.0, value=1000.0, step=100.0, format="%.2f")
    tasa_anual = st.number_input("Tasa anual (%)", min_value=0.0, value=12.0, step=0.5, format="%.2f")
    plazo = st.number_input("Plazo", min_value=1, value=12, step=1)
    unidad_plazo = st.selectbox("Unidad del plazo", ["Meses", "Años"])
    tipo_interes = st.selectbox("Tipo de interés", ["Interés simple", "Interés compuesto"])
    frecuencia = st.selectbox("Frecuencia de capitalización", ["Mensual", "Trimestral", "Semestral", "Anual"])
    st.caption("La frecuencia se usa para interés compuesto.")

frecuencias = {
    "Mensual": 12,
    "Trimestral": 4,
    "Semestral": 2,
    "Anual": 1,
}

tiempo_anios = plazo / 12 if unidad_plazo == "Meses" else plazo
tasa_decimal = tasa_anual / 100
n = frecuencias[frecuencia]

if tipo_interes == "Interés simple":
    monto_final = capital * (1 + tasa_decimal * tiempo_anios)
    formula = "M = C × (1 + i × t)"
else:
    monto_final = capital * (1 + tasa_decimal / n) ** (n * tiempo_anios)
    formula = "M = C × (1 + i/n)^(n×t)"

interes_generado = monto_final - capital
rentabilidad = (interes_generado / capital * 100) if capital > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Monto final", f"${monto_final:,.2f}")
col2.metric("Interés generado", f"${interes_generado:,.2f}")
col3.metric("Rentabilidad", f"{rentabilidad:,.2f}%")

st.markdown("### Fórmula aplicada")
st.markdown(
    f"""
    <div class="formula-box">
    <b>{tipo_interes}</b><br>
    Fórmula: <code>{formula}</code><br>
    Capital: <code>${capital:,.2f}</code> · Tasa anual: <code>{tasa_anual:.2f}%</code> · Tiempo: <code>{tiempo_anios:.2f} años</code>
    </div>
    """,
    unsafe_allow_html=True,
)

periodos = max(1, int(math.ceil(tiempo_anios * 12)))
filas = []
for mes in range(0, periodos + 1):
    t = mes / 12
    if tipo_interes == "Interés simple":
        monto = capital * (1 + tasa_decimal * t)
    else:
        monto = capital * (1 + tasa_decimal / n) ** (n * t)
    filas.append({
        "mes": mes,
        "años": round(t, 2),
        "monto_acumulado": round(monto, 2),
        "interes_acumulado": round(monto - capital, 2),
    })

df = pd.DataFrame(filas)

st.markdown("### Evolución del monto")
fig = px.line(
    df,
    x="mes",
    y="monto_acumulado",
    markers=True,
    title="Crecimiento del capital en el tiempo",
)
fig.update_layout(xaxis_title="Mes", yaxis_title="Monto acumulado")
st.plotly_chart(fig, use_container_width=True)

st.markdown("### Tabla de simulación")
st.dataframe(df, use_container_width=True)

csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    "Descargar simulación en CSV",
    data=csv,
    file_name="simulacion_interes.csv",
    mime="text/csv",
)

st.info(
    "Reto sugerido: agrega una tercera opción para comparar interés simple vs. compuesto en un solo gráfico."
)
