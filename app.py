from flask import Flask, render_template, request, redirect, session, url_for
from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from bilstm_model import predict_disease
import io, os
app = Flask(__name__)
app.secret_key = "supersecretkey"

# Disease database
disease_db = {
    "cold": {"treatment": "Take paracetamol and rest for 2-3 days.", "doctor": "Dr. Rajesh Kumar", "degree": "MD", "hospital": "City Hospital", "phone": "9876543210", "icon":"cold.png"},
    "cough": {"treatment": "Cough syrup twice a day.", "doctor": "Dr. Meena Sharma", "degree": "MD", "hospital": "Green Clinic", "phone": "9876501234", "icon":"cough.png"},
    "fever": {"treatment": "Paracetamol every 6-8 hours.", "doctor": "Dr. Ramesh Singh", "degree": "PhD", "hospital": "Central Hospital", "phone": "9876540000", "icon":"fever.png"},
    "diabetes": {"treatment": "Monitor blood sugar, take Metformin.", "doctor": "Dr. Anil Patel", "degree": "MD", "hospital": "LifeCare Hospital", "phone": "9876004321", "icon":"diabetes.png"},
    "hypertension": {"treatment": "Take prescribed BP medicines daily.", "doctor": "Dr. Priya Nair", "degree": "MD", "hospital": "HealthPlus Clinic", "phone": "9876023456", "icon":"hypertension.png"},
    "asthma": {"treatment": "Use inhaler as prescribed.", "doctor": "Dr. Sanjay Verma", "degree": "MD", "hospital": "BreathWell Hospital", "phone": "9876034567", "icon":"asthma.png"},
    "migraine": {"treatment": "Take Ibuprofen/Paracetamol during attacks.", "doctor": "Dr. Shalini Gupta", "degree": "MD", "hospital": "NeuroCare Hospital", "phone": "9876045678", "icon":"migraine.png"},
    "allergy": {"treatment": "Take antihistamine tablets.", "doctor": "Dr. Vikram Yadav", "degree": "PhD", "hospital": "Allergy Care Clinic", "phone": "9876056789", "icon":"allergy.png"},
    "stomach pain": {"treatment": "Take antacid before meals.", "doctor": "Dr. Sunita Rao", "degree": "MD", "hospital": "Digestive Care Hospital", "phone": "9876067890", "icon":"stomach_pain.png"},
    "overweight": {"treatment": "Follow low-carb diet, exercise regularly.", "doctor": "Dr. Kavita Menon", "degree": "MD", "hospital": "Wellness Clinic", "phone": "9876012345", "icon":"overweight.png"},
    "thyroid": {"treatment": "Take prescribed thyroid medicine.", "doctor": "Dr. Nikhil Agarwal", "degree": "MD", "hospital": "Endocrine Center", "phone": "9876078901", "icon":"thyroid.png"},
    "arthritis": {"treatment": "Take anti-inflammatory medicines.", "doctor": "Dr. Ritu Sharma", "degree": "MD", "hospital": "OrthoCare Hospital", "phone": "9876089012", "icon":"arthritis.png"},
    "skin infection": {"treatment": "Apply topical antibiotics.", "doctor": "Dr. Akash Mehta", "degree": "MD", "hospital": "SkinCare Clinic", "phone": "9876090123", "icon":"skin_infection.png"},
    "flu": {"treatment": "Take antiviral medicines.", "doctor": "Dr. Pooja Reddy", "degree": "MD", "hospital": "FluCare Hospital", "phone": "9876101234", "icon":"flu.png"},
    "back pain": {"treatment": "Take pain relievers, physiotherapy.", "doctor": "Dr. Vivek Joshi", "degree": "MD", "hospital": "SpineCare Hospital", "phone": "9876112345", "icon":"back_pain.png"}
}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        session["patient"] = {
            "first_name": request.form["first_name"],
            "last_name": request.form["last_name"],
            "age": request.form["age"],
            "gender": request.form["gender"],
            "phone": request.form["phone"],
            "address": request.form["address"]
        }
        return redirect(url_for("physical"))
    return render_template("home.html")

@app.route("/physical", methods=["GET", "POST"])
def physical():
    if request.method == "POST":
        session["physical"] = {
            "height": request.form["height"],
            "weight": request.form["weight"],
            "bp": request.form["bp"],
            "heart_rate": request.form["heart_rate"],
            "allergies": request.form["allergies"],
            "habits": request.form["habits"]
        }
        return redirect(url_for("disease"))
    return render_template("physical.html")

@app.route("/disease", methods=["GET","POST"])
def disease():
    if request.method=="POST":
        selected_disease = request.form.get("disease")

# AI prediction (for explanation / chatbot)
        symptoms = " ".join(request.form.values())
        ai_prediction = predict_disease(symptoms)

        session["disease"] = {
            "disease": selected_disease,
            "ai_prediction": ai_prediction
        }
        return redirect(url_for("advice"))
    return render_template("disease.html", diseases=disease_db)

@app.route("/advice")
def advice():
    selected_disease = session.get("disease", {}).get("disease")
    info = disease_db.get(selected_disease, {})
    return render_template("advice.html", patient=session.get("patient"), disease=session.get("disease"), info=info)

@app.route('/download_report')
def download_report():
    buffer = io.BytesIO()

    # Custom watermark function
    def add_watermark(canvas, doc):
        # Semi-transparent hospital watermark in the background
        canvas.saveState()
        canvas.setFont('Helvetica-Bold', 60)
        canvas.setFillColorRGB(0.9, 0.9, 0.9, alpha=0.2)  # light gray transparent
        canvas.drawCentredString(A4[0]/2, A4[1]/2, "City Hospital")
        canvas.restoreState()

    # Build PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # --- Logo or stethoscope image ---
    stethoscope_path = os.path.join("static", "images", "stethoscope.png")
    if os.path.exists(stethoscope_path):
        elements.append(Image(stethoscope_path, width=1.2*inch, height=1.2*inch))
    elements.append(Paragraph("<b>Final Health Report</b>", styles['Title']))
    elements.append(Spacer(1, 12))

    # Patient details
    elements.append(Paragraph("<b>Patient Details</b>", styles['Heading2']))
    p = session.get("patient", {})
    patient_data = [
        ["Name", f"{p.get('first_name')} {p.get('last_name')}"],
        ["Age", p.get("age")],
        ["Gender", p.get("gender")],
        ["Phone", p.get("phone")],
        ["Address", p.get("address")]
    ]

    t = Table(patient_data, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica')
    ]))
    elements.append(t)
    elements.append(Spacer(1, 12))

    # Physical details
    elements.append(Paragraph("<b>Physical Details</b>", styles['Heading2']))
    ph = session.get("physical", {})
    physical_data = [
        ["Height", ph.get("height")],
        ["Weight", ph.get("weight")],
        ["BP", ph.get("bp")],
        ["Heart Rate", ph.get("heart_rate")],
        ["Allergies", ph.get("allergies")],
        ["Habits", ph.get("habits")]
    ]
    t2 = Table(physical_data, hAlign='LEFT')
    t2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica')
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 12))

    # Disease info
    d = session.get("disease", {})
    info = disease_db.get(d.get("disease"), {})
    elements.append(Paragraph("<b>Your Disease</b>", styles['Heading2']))
    elements.append(Paragraph(f"Disease: {d.get('disease')}", styles['Normal']))

    # Treatment advice
    elements.append(Paragraph("<b>Treatment Advice</b>", styles['Heading2']))
    elements.append(Paragraph(f"Treatment: {info.get('treatment')}", styles['Normal']))
    elements.append(Spacer(1, 12))

    # Doctor info
    elements.append(Paragraph("<b>Doctor Information</b>", styles['Heading2']))
    elements.append(Paragraph(f"Name: {info.get('doctor')}", styles['Normal']))
    elements.append(Paragraph(f"Hospital: {info.get('hospital')}", styles['Normal']))
    elements.append(Paragraph(f"Phone: {info.get('phone')}", styles['Normal']))

    # Generate PDF with watermark
    doc.build(elements, onFirstPage=add_watermark, onLaterPages=add_watermark)

    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="Health_Report.pdf", mimetype='application/pdf')
@app.route("/ai_chat", methods=["POST"])
def ai_chat():
    user_text = request.json.get("text","")

    predicted = predict_disease(user_text)
    info = disease_db.get(predicted, {})

    reply = f"""
AI Prediction: {predicted.upper()}
Suggested Treatment: {info.get('treatment')}
Doctor: {info.get('doctor')}
Hospital: {info.get('hospital')}
Phone: {info.get('phone')}
"""

    return {"reply": reply}

if __name__ == "__main__":
    app.run(debug=True)
