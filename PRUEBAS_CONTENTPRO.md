# 📋 GUÍA DE PRUEBAS — ContentPro App
**Archivo:** `index.html` | **Fecha:** 2026-05-14  
**URL local:** `file:///C:/Users/Yudy Rodriguez F/.claude/projects/web/index.html`

---

## ✅ PRE-REQUISITOS (hacer primero)

Antes de probar cualquier módulo configura estas API keys en **Cuentas**:

| API Key | Dónde obtenerla | Para qué sirve |
|---|---|---|
| Groq API Key | console.groq.com → API Keys (gratis) | Generar texto, carruseles, guiones |
| OpenAI API Key | platform.openai.com/api-keys | Imágenes gpt-image-1 (opcional) |
| YouTube refresh token | Ya configurado | Publicar videos |

**Cómo guardar las keys:**
1. Ir a sección **Cuentas** (menú lateral)
2. Pegar cada key en su campo
3. Click **Guardar** → debe mostrar ✅ verde

---

## 🧬 MÓDULO 1 — ADN DE MARCA

**Sección:** `ADN de Marca` en el menú lateral  
**Propósito:** Define el perfil de tu marca — nombre, tono, colores, industria.

### Pasos de prueba:
1. **Ir a ADN de Marca**
2. Llenar los campos:
   - Nombre de marca: `Dykan Project`
   - Industria: `Marketing Digital`
   - Tono: `Profesional y cercano`
   - Bio de Instagram: (pegar bio real)
3. Click **Analizar** → debe generar descripción de marca con Groq
4. **Resultado esperado:** Aparece perfil de marca con colores sugeridos, tono, hashtags detectados
5. ✅ **Verificar:** La info se guarda y aparece pre-llenada en otros módulos

---

## 🎠 MÓDULO 2 — CARRUSELES DE INSTAGRAM

**Sección:** `Carruseles` en el menú  
**Propósito:** Genera carruseles profesionales con texto + imágenes para Instagram

### PASO 2.1 — Generar carrusel con IA

1. **Ir a Carruseles**
2. En el campo **Tema:** escribir → `"5 errores que cometen los emprendedores"`
3. Seleccionar **Tono:** `Educativo`
4. Seleccionar **Estilo visual:** `gold` (u otro)
5. Click **✨ Generar Carrusel** (botón principal dorado)
6. **Resultado esperado:** Panel derecho muestra 7 slides con título + texto por cada una
7. ✅ **Verificar:** Aparecen bullets de navegación (dots) y miniatura de cada slide

---

### PASO 2.2 — Imágenes GRATIS con Pollinations (sin API key)

1. Tener el carrusel generado (paso 2.1)
2. En panel **📸 Imágenes IA** → click **🌸 Imágenes GRATIS (FLUX)**
3. **Resultado esperado:** 
   - Aparece panel modal mostrando 7 filas (una por slide)
   - Cada fila cambia de "⏳ En cola…" → "⚡ Generando…" → "✅ Lista"
   - Las imágenes aparecen en las miniaturas (~8-15 segundos por imagen)
4. ✅ **Verificar:** La vista previa central muestra la imagen en el slide activo
5. ❌ **Si falla:** La imagen es nil en Pollinations → reintenta automáticamente 1 vez

---

### PASO 2.3 — Imágenes con ChatGPT (8 gratis por día)

1. Tener el carrusel generado
2. Click **🤖 ChatGPT (8 gratis)** 
3. **Resultado esperado:** Abre el wizard con una card por cada slide
4. Click **🚀 Abrir TODAS en ChatGPT** (footer del wizard)
5. **Resultado esperado:** Se abren N pestañas de Chrome, cada una con `chatgpt.com` y el prompt ya escrito en el chat
6. En cada pestaña: presionar **Enter** → esperar imagen → descargar (click derecho → Guardar imagen)
7. Volver al wizard → arrastra o sube la imagen descargada en la zona de la slide correspondiente
8. **Resultado esperado:** 
   - Imagen aparece en la slide
   - Badge cambia a ✅
   - Se genera automáticamente: caption de Instagram + hashtags (con Groq)
9. ✅ **Verificar:** Contador diario se actualiza (ej: "3 / 8 imágenes usadas hoy")

---

### PASO 2.4 — Imágenes con gpt-image-1 (requiere OpenAI key)

1. Tener OpenAI key configurada en Cuentas
2. Click **✨ gpt-image-1 (OpenAI)**
3. **Resultado esperado:** Modal "gpt-image-1 — X imágenes" con barra de progreso
4. Genera automáticamente todas las imágenes (~15-20s por imagen)
5. ✅ **Verificar:** Imágenes de mayor calidad vs Pollinations

> ⚠️ **Si no hay key:** Aparece popup ofreciendo usar Pollinations gratis

---

### PASO 2.5 — Exportar carrusel

Opciones en sección **💾 Exportar**:

| Botón | Prueba | Resultado esperado |
|---|---|---|
| 📥 PNGs | Click → descarga | Se descarga un .zip con cada slide como PNG |
| 💾 Guardar | Click | Carrusel guardado en biblioteca local |
| 📊 Sheets | Click | Copia datos tabulados listos para pegar en Google Sheets |
| 📸 PNG (slide actual) | Click en vista previa | Descarga la slide actual como PNG |

---

### PASO 2.6 — Enviar a Cola de Publicación

1. Tener al menos una imagen en el carrusel
2. Click **📋 Enviar a Cola de Publicación →**
3. **Resultado esperado:** 
   - Si hay Groq key → verifica coherencia de imágenes primero
   - Navega automáticamente a sección **Cola**
   - Aparece el carrusel como tarjeta con preview, caption y hashtags
4. ✅ **Verificar:** El carrusel aparece en "⏳ Pendiente de aprobación"

---

## 📱 MÓDULO 3 — VIDEOS / REELS

**Sección:** `Videos` en el menú  
**Propósito:** Genera scripts y estructura para Reels de Instagram / YouTube Shorts

### Pasos de prueba:
1. **Ir a Videos**
2. Escribir tema: `"Cómo conseguir tus primeros 1000 seguidores"`
3. Seleccionar plataforma: `Instagram Reels`
4. Seleccionar duración: `30 segundos`
5. Click **✨ Generar Script**
6. **Resultado esperado:** Script dividido en: Hook (3s) + Desarrollo + CTA final
7. ✅ **Verificar:** Texto listo para grabar, con tiempos por segmento
8. Click **📋 Enviar a Cola →** → aparece en Cola como tipo "reel"

---

## 💼 MÓDULO 4 — LINKEDIN

**Sección:** `LinkedIn` en el menú  
**Propósito:** Genera posts profesionales optimizados para LinkedIn

### Pasos de prueba:
1. **Ir a LinkedIn**
2. Escribir tema: `"Lección que aprendí al escalar mi negocio"`
3. Seleccionar formato: `Historia personal` (o el que prefieras)
4. Click **✨ Generar Post**
5. **Resultado esperado:** Post con estructura: Hook + historia + aprendizaje + CTA + hashtags
6. ✅ **Verificar:** Máx ~1300 caracteres, formato LinkedIn nativo
7. Click **📋 Enviar a Cola →**

---

## 📝 MÓDULO 5 — GUIONES

**Sección:** `Guiones` en el menú  
**Propósito:** Genera guiones completos para videos largos, podcasts o presentaciones

### Pasos de prueba:
1. **Ir a Guiones**
2. Escribir tema: `"Tutorial: Cómo usar IA para tu negocio"`
3. Seleccionar tipo: `YouTube (video largo)`
4. Duración estimada: `10 minutos`
5. Click **✨ Generar Guión**
6. **Resultado esperado:** Guión completo con intro, secciones numeradas, transiciones y outro
7. ✅ **Verificar:** Incluye indicaciones de cámara / ritmo de presentación
8. Click **📋 Enviar a Cola →**

---

## ⚡ MÓDULO 6 — HORMOZI CONTENT

**Sección:** `Hormozi` en el menú  
**Propósito:** Genera contenido usando el framework de Alex Hormozi (educativo + ventas)

### Pasos de prueba:
1. **Ir a Hormozi**
2. Escribir oferta/producto: `"Consultoría de marketing digital"`
3. Click **⚡ Generar pack Hormozi**
4. **Resultado esperado:** Pack completo con:
   - Post de valor (educativo)
   - Reel script agresivo de ventas
   - Caption de Instagram listo
   - Post LinkedIn
   - Stories CTAs
5. ✅ **Verificar:** Todo el pack aparece con botón **Enviar a Cola**

---

## 💡 MÓDULO 7 — IDEAS DE CONTENIDO

**Sección:** `Ideas` en el menú  
**Propósito:** Genera banco de ideas para los próximos 30 días

### Pasos de prueba:
1. **Ir a Ideas**
2. Escribir nicho/industria: `"Emprendimiento y marketing"`
3. Click **Generar ideas**
4. **Resultado esperado:** Lista de 10-20 ideas con formato, plataforma sugerida y nivel de engagement esperado
5. ✅ **Verificar:** Cada idea tiene botón para "Crear contenido" que lleva al módulo correspondiente

---

## 📅 MÓDULO 8 — CALENDARIO DE CONTENIDO

**Sección:** `Calendario` en el menú  
**Propósito:** Vista del contenido programado por semana/mes

### Pasos de prueba:
1. **Ir a Calendario**
2. ✅ **Verificar:** Muestra los items enviados a Cola en sus fechas correspondientes
3. Click en cualquier día con contenido → debe mostrar preview del item

---

## 📊 MÓDULO 9 — MÉTRICAS

**Sección:** `Métricas` en el menú  
**Propósito:** Dashboard con estadísticas de contenido generado

### Pasos de prueba:
1. **Ir a Métricas**
2. ✅ **Verificar:** Muestra:
   - Total de piezas generadas
   - Distribución por plataforma
   - Carruseles creados esta semana
3. ✅ **Verificar:** Los números se actualizan después de generar contenido

---

## 📋 MÓDULO 10 — COLA DE PUBLICACIÓN

**Sección:** `Cola` en el menú  
**Propósito:** Gestionar y aprobar todo el contenido antes de publicar

### Pasos de prueba:
1. **Ir a Cola** (después de haber enviado items desde otros módulos)
2. ✅ **Verificar:** Aparecen todas las piezas con:
   - Tipo (🎠 carrusel / 🎬 video / 💼 linkedin)
   - Preview (imagen o texto)
   - Caption e hashtags
   - Fecha y hora
3. **Probar botones por item:**
   - 📋 **Copiar caption** → debe copiar al portapapeles
   - ✅ **Aprobar** → mueve a "Publicados"
   - 🗑️ **Eliminar** → quita de la cola
4. ✅ **Verificar:** Sección muestra separado: "Pendiente" y "Publicados"

---

## 🎬 MÓDULO 11 — VIDEO LARGO

**Sección:** `Video Largo` en el menú  
**Propósito:** Generador de videos largos con múltiples clips y narración

### Pasos de prueba:
1. **Ir a Video Largo**
2. Escribir tema o usar episodio del calendario
3. Click **Generar clips**
4. ✅ **Verificar:** Genera imágenes con Pollinations + animación Ken Burns + narración EdgeTTS
5. ✅ **Verificar:** Video final se ensambla con transiciones y música

---

## 🔑 MÓDULO 12 — CUENTAS / CONFIGURACIÓN

**Sección:** `Cuentas` en el menú  
**Propósito:** Gestionar todas las API keys y conexiones

### Pasos de prueba:
1. **Ir a Cuentas**
2. **Probar cada sección:**

| Campo | Valor de prueba | Verificación esperada |
|---|---|---|
| Groq API Key | `gsk_...` | ✅ Verde con nombre del modelo |
| OpenAI API Key | `sk-...` | ✅ Verde con saldo disponible |
| YouTube | Token guardado | ✅ Canal conectado |
| Instagram | - | ⚠️ Pendiente configurar |
| Facebook | - | ⚠️ Pendiente configurar |

---

## 🤖 MÓDULO 13 — VIDEO FACTORY (Node.js — Terminal)

**Ubicación:** `C:\Users\Yudy Rodriguez F\.claude\projects\web\pruebas\video_factory\`  
**Propósito:** Pipeline automático diario → genera + publica episodios de OMNIPRESENTE

### Comandos de prueba:

```bash
# Abrir terminal en la carpeta:
cd "C:\Users\Yudy Rodriguez F\.claude\projects\web\pruebas\video_factory"

# 1. Ver estado del calendario
node scheduler.js status

# 2. Probar el pipeline SIN publicar (dry-run)
node scheduler.js run-now --dry-run

# 3. Ejecutar episodio específico en dry-run
node scheduler.js run-episode 1 --dry-run

# 4. Ejecutar episodio real (genera + publica a YouTube)
node scheduler.js run-episode 1

# 5. Verificar el log del sistema
type scheduler.log
```

### Verificaciones:
- ✅ `status` muestra los 30 episodios con fechas y estados
- ✅ `run-now --dry-run` genera imágenes + video pero NO publica
- ✅ `run-episode 1` genera video EP1 y lo sube a YouTube
- ✅ Video aparece en https://youtube.com/@tucanal

---

## 🧪 PRUEBA INTEGRAL — Flujo completo de punta a punta

### Scenario: "Crear y publicar un carrusel completo"

1. **ADN de Marca** → Llenar perfil de Dykan Project
2. **Carruseles** → Generar carrusel sobre "5 tips de productividad"
3. **Imágenes** → Click "🌸 Imágenes GRATIS" → esperar 7 imágenes
4. **Revisar** → Navegar por las slides con las flechas ← →
5. **Exportar** → Descargar como PNGs (verificar que se descarga .zip)
6. **Cola** → Click "📋 Enviar a Cola" → verificar que aparece en Cola
7. **Cola** → Copiar caption → pegar en Instagram manualmente

### Scenario: "Usar ChatGPT para las imágenes"

1. **Carruseles** → Generar carrusel (cualquier tema)
2. Click **🤖 ChatGPT (8 gratis)** → abre wizard
3. Click **🚀 Abrir TODAS en ChatGPT** → verificar que abren N pestañas
4. En ChatGPT: presionar Enter → generar imagen → descargar
5. Volver al wizard → subir imagen en la slide correcta
6. ✅ Verificar que aparecen caption + hashtags generados automáticamente
7. Repetir para las 8 imágenes del día

---

## ❌ ERRORES COMUNES Y SOLUCIONES

| Error | Causa | Solución |
|---|---|---|
| "Groq key no configurada" | API key vacía | Ir a Cuentas → pegar la key |
| Imágenes no cargan en Pollinations | Timeout / conexión | Esperar 30s y reintentar |
| ChatGPT dice "límite alcanzado" | 8 imágenes/día ya usadas | Esperar hasta medianoche o usar Pollinations |
| "No se puede acceder a este sitio" en Chrome | URL sin `file:///` | Escribir la URL completa con `file:///` |
| Video factory: "No episode pending" | Fecha del calendario incorrecta | Verificar calendar.json o usar `run-episode N` |
| Instagram/Facebook: "not configured" | Tokens no guardados | Configurar tokens en social_tokens.json |

---

## 📁 ARCHIVOS CLAVE DEL PROYECTO

```
projects/web/
├── index.html                    ← App principal (todo el frontend)
└── pruebas/video_factory/
    ├── config.js                 ← API keys y configuración
    ├── calendar.json             ← 30 episodios programados
    ├── scheduler.js              ← Cron diario 12pm
    ├── image-video.js            ← Genera imágenes + animación
    ├── video-assembler.js        ← Ensambla video final con ffmpeg
    ├── social-publisher.js       ← Publica a YouTube/Instagram/Facebook
    ├── prompt-enhancer.js        ← Mejora prompts con Groq
    ├── content-calendar.js       ← Genera calendario con Groq
    └── output/                   ← Videos generados
```

---

*Documento generado: 2026-05-14 | ContentPro v1.0*
