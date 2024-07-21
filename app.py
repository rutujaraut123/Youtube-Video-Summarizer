from flask import Flask, render_template, request, make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO  # Add this import statement
from youtube_transcript_api import YouTubeTranscriptApi
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
app = Flask(__name__)

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    link = request.form['link']
    video_id = link.split("/")[-1].split("?")[0]

    try:
        # Retrieve transcript for Hindi language ('hi')
        hindi_transcript_obj = YouTubeTranscriptApi.get_transcript(video_id, languages=['hi'])
        hindi_transcript = " ".join([sub["text"] for sub in hindi_transcript_obj])

        return render_template('transcript.html', transcript=hindi_transcript)

    except Exception as hindi_error:
        try:
            # Retrieve transcript for English language ('en')
            english_transcript_obj = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
            english_transcript = " ".join([sub["text"] for sub in english_transcript_obj])

            return render_template('transcript.html', transcript=english_transcript)

        except Exception as english_error:
            return "Error retrieving transcript: " + str(english_error)

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    # Get the transcript text from the form data
    transcript_text = request.form['transcript']

    # Generate PDF from transcript text using ReportLab
    pdf_content = generate_pdf_reportlab(transcript_text)

    # Create response with PDF content
    response = make_response(pdf_content)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=transcript.pdf'

    return response

def generate_pdf_reportlab(transcript_text):
    # Create PDF document
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Create a list of Paragraph objects from the transcript text
    elements = []
    for line in transcript_text.split('\n'):
        elements.append(Paragraph(line, styles["BodyText"]))

    # Build the PDF document
    doc.build(elements)

    # Return PDF content
    pdf_content = buffer.getvalue()
    buffer.close()
    return pdf_content
if __name__ == '__main__':
    app.run(debug=True)