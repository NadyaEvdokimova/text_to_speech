from voice_converter import VoiceConverter, VoiceConverterError
from datetime import datetime
from flask import Flask, render_template, url_for, redirect, send_file, Response, flash, get_flashed_messages, jsonify
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired
import os

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
audio_generated = False


class TextForm(FlaskForm):
    text = StringField("Text to convert", validators=[DataRequired()])
    voice = SelectField("Choose voice", choices=["Nancy", "Alice", "Lily", "Harry"])
    submit = SubmitField('Convert to speech')


@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}


@app.route('/', methods=["GET", "POST"])
def home():
    global audio_generated
    form = TextForm()
    if form.validate_on_submit():
        text_to_convert = form.text.data
        voice = form.voice.data
        try:
            converter = VoiceConverter(text_to_convert, voice)
            audio_generated = True
            return Response(converter.response.content, headers={
                'Content-Type': 'audio/mpeg',
                'Content-Disposition': 'attachment; filename="music.mp3"',
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            })
        except VoiceConverterError as e:
            flash(str(e), "error")
            print("except case")
            return redirect(url_for('home'))
    return render_template("index.html", form=form)


@app.route('/audio')
def audio():
    if audio_generated:
        return send_file('music.mp3', as_attachment=True)
    else:
        return redirect(url_for('home'))


@app.route('/get_flashed_messages_json')
def get_flashed_messages_json():
    messages = get_flashed_messages(with_categories=True)
    print(f"message: {messages}")
    return jsonify([{'message': message[1], 'category': message[0]} for message in messages])


if __name__ == "__main__":
    app.run(debug=True, port=5001)
