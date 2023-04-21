import whisper

def audioToText(audioPath): 
    model = whisper.load_model("base")
    # load audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(audioPath)
    audio = whisper.pad_or_trim(audio)

    # make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # decode the audio
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    text = result.text

    # return the recognized text
    return text