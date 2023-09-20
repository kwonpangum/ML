from flask import Flask, request, jsonify, make_response
import tensorflow as tf
from models import create_model
from hparams import hparams
from text import text_to_sequence
from audio import inv_spectrogram, inv_preemphasis
from scipy.io.wavfile import write
import numpy as np

app = Flask(__name__)

# Load the model
checkpoint_path = "checkpoint_path"
model_name = "Tacotron"
inputs = tf.placeholder(tf.int32, [1, None], 'inputs')
input_lengths = tf.placeholder(tf.int32, [1], 'input_lengths')
speaker_id = tf.placeholder(tf.int32, [1], 'speaker_id')
with tf.variable_scope('model') as scope:
    model = create_model(hparams)
    model.initialize(inputs, input_lengths, speaker_id)
sess = tf.Session()
sess.run(tf.global_variables_initializer())
saver = tf.train.Saver()
load_checkpoint(sess, saver, checkpoint_path)

# Define routes
@app.route('/synthesize', methods=['POST'])
def synthesize():
    # Get text input
    text = request.form['text']

    # Convert text to sequence
    cleaner_names = [x.strip() for x in hparams.cleaners.split(',')]
    seq = text_to_sequence(text.strip(), cleaner_names)

    # Synthesize
    mel_outputs, linear_outputs, alignments = sess.run(
        [model.mel_outputs, model.linear_outputs, model.alignments],
        feed_dict={
            inputs: [np.asarray(seq, dtype=np.int32)],
            input_lengths: np.asarray([len(seq)], dtype=np.int32),
            speaker_id: np.asarray([0], dtype=np.int32),
        })

    # Convert spectrogram to waveform using Griffin-Lim
    signal = inv_preemphasis(inv_spectrogram(linear_outputs[0].T ** hparams.power), hparams.preemphasis)
    signal /= np.max(np.abs(signal))

    # Save audio file
    write('output.wav', hparams.sample_rate, signal)

    # Return audio file as response
    with open('output.wav', 'rb') as f:
        audio_bytes = f.read()
    response = make_response(audio_bytes)
    response.headers.set('Content-Type', 'audio/wav')
    response.headers.set('Content-Disposition', 'attachment', filename='output.wav')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
