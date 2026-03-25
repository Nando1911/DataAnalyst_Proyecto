import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Ventas", layout="wide")

st.title("📊 Dashboard de Ventas Profesional - Portafolio")

# --- Cargar datos ---
data = pd.read_csv("ventas.csv")
data['fecha'] = pd.to_datetime(data['fecha'])
data['ingresos'] = data['ventas'] * data['precio']

# --- Filtros ---
col1, col2 = st.columns(2)
with col1:
    producto_seleccionado = st.selectbox("Selecciona un producto", data['producto'].unique())
with col2:
    fecha_inicio = st.date_input("Fecha inicio", data['fecha'].min())
    fecha_fin = st.date_input("Fecha fin", data['fecha'].max())

data_filtrada = data[(data['producto'] == producto_seleccionado) &
                     (data['fecha'] >= pd.to_datetime(fecha_inicio)) &
                     (data['fecha'] <= pd.to_datetime(fecha_fin))]

# --- KPIs ---
ingresos_totales = data_filtrada['ingresos'].sum()
ingreso_max_dia = data_filtrada.groupby('fecha')['ingresos'].sum().max() if not data_filtrada.empty else 0
dia_max_ingreso = data_filtrada.groupby('fecha')['ingresos'].sum().idxmax() if not data_filtrada.empty else None
ventas_totales = data_filtrada['ventas'].sum()
ventas_promedio = data_filtrada['ventas'].mean() if not data_filtrada.empty else 0
producto_top = data_filtrada.groupby('producto')['ingresos'].sum().idxmax() if not data_filtrada.empty else None

st.subheader("💰 Métricas Clave")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Ingresos Totales", f"${ingresos_totales:.2f}")
kpi2.metric("Día con Mayor Ingreso", f"{dia_max_ingreso.date() if dia_max_ingreso else '-'}", f"${ingreso_max_dia:.2f}")
kpi3.metric("Ventas Totales", f"{ventas_totales}")
kpi4.metric("Ventas Promedio Diarias", f"{ventas_promedio:.2f}")

st.write(f"**Producto Top en ingresos:** {producto_top if producto_top else '-'}")

# --- Gráfico de ingresos por producto ---
fig1 = px.bar(data_filtrada.groupby('producto')['ingresos'].sum().reset_index(),
              x='producto', y='ingresos', color='ingresos',
              color_continuous_scale='Viridis', title="📊 Ventas por Producto")
st.plotly_chart(fig1, use_container_width=True)

# --- Gráfico de ingresos en el tiempo ---
fig2 = px.line(data_filtrada.groupby('fecha')['ingresos'].sum().reset_index(),
               x='fecha', y='ingresos', markers=True,
               title="📈 Tendencia de Ingresos en el Tiempo")
fig2.update_layout(xaxis_title="Fecha", yaxis_title="Ingresos ($)")
st.plotly_chart(fig2, use_container_width=True)

# --- Tabla de datos ---
st.subheader("📄 Datos Filtrados")
st.dataframe(data_filtrada)

# --- Insights automáticos ---
st.subheader("💡 Insights Automáticos")
if data_filtrada.empty:
    st.write("⚠️ No hay datos en el rango seleccionado.")
else:
    if ingresos_totales > 1000:
        st.write("✅ Excelente: los ingresos son altos en este periodo.")
    else:
        st.write("⚠️ Los ingresos son bajos, considera revisar estrategias de ventas.")
    if ventas_promedio > 5:
        st.write(f"💡 En promedio se venden {ventas_promedio:.2f} unidades diarias del producto {producto_seleccionado}.")
    else:
        st.write(f"💡 Ventas promedio bajas, analizar promociones para {producto_seleccionado}.")