import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment
import noisereduce as nr
from scipy import signal

class AudioProcessor:
    def __init__(self):
        self.sample_rate = 44100

    def process(self, input_path: str, output_path: str, song_style: str = "none", voice_style: str = "natural"):
        """处理音频文件"""
        try:
            y, sr = librosa.load(input_path, sr=self.sample_rate)

            y = self.reduce_noise(y, sr)

            y = self.pitch_correction(y, sr, song_style)

            y = self.apply_voice_style(y, sr, voice_style)

            y = self.normalize_audio(y)

            sf.write(output_path, y, sr)

        except Exception as e:
            raise Exception(f"音频处理失败: {str(e)}")

    def reduce_noise(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """降噪处理"""
        try:
            reduced = nr.reduce_noise(y=audio, sr=sr, prop_decrease=0.8)
            return reduced
        except:
            return audio

    def pitch_correction(self, audio: np.ndarray, sr: int, song_style: str) -> np.ndarray:
        """音高校正"""
        try:
            pitches, magnitudes = librosa.piptrack(y=audio, sr=sr)

            pitch_shift_steps = self.get_pitch_shift_for_style(song_style)

            if pitch_shift_steps != 0:
                audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=pitch_shift_steps)

            f0 = librosa.yin(audio, fmin=librosa.note_to_hz('C2'),
                            fmax=librosa.note_to_hz('C7'), sr=sr)

            f0_corrected = self.quantize_to_scale(f0)

            return audio

        except Exception as e:
            print(f"音高校正警告: {e}")
            return audio

    def get_pitch_shift_for_style(self, song_style: str) -> float:
        """根据歌曲风格获取音高偏移"""
        style_map = {
            "pop": 0,
            "rock": 0.5,
            "jazz": -0.5,
            "classical": 0,
            "electronic": 1,
            "none": 0
        }
        return style_map.get(song_style, 0)

    def quantize_to_scale(self, f0: np.ndarray) -> np.ndarray:
        """将音高量化到最近的音符"""
        f0_corrected = f0.copy()
        valid = f0 > 0

        if np.any(valid):
            midi_notes = librosa.hz_to_midi(f0[valid])
            rounded_notes = np.round(midi_notes)
            f0_corrected[valid] = librosa.midi_to_hz(rounded_notes)

        return f0_corrected

    def apply_voice_style(self, audio: np.ndarray, sr: int, voice_style: str) -> np.ndarray:
        """应用音色风格"""
        try:
            if voice_style == "natural":
                return audio

            elif voice_style == "smooth":
                b, a = signal.butter(4, 3000 / (sr / 2), 'low')
                audio = signal.filtfilt(b, a, audio)
                audio = self.add_reverb(audio, sr, 0.3)

            elif voice_style == "powerful":
                audio = audio * 1.2
                audio = self.enhance_bass(audio, sr)

            elif voice_style == "bright":
                b, a = signal.butter(2, 2000 / (sr / 2), 'high')
                audio = signal.filtfilt(b, a, audio)
                audio = audio * 1.1

            elif voice_style == "warm":
                audio = self.enhance_bass(audio, sr)
                b, a = signal.butter(2, 8000 / (sr / 2), 'low')
                audio = signal.filtfilt(b, a, audio)

            elif voice_style == "auto":
                audio = self.auto_enhance(audio, sr)

            return audio

        except Exception as e:
            print(f"音色处理警告: {e}")
            return audio

    def enhance_bass(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """增强低音"""
        b, a = signal.butter(4, 300 / (sr / 2), 'low')
        bass = signal.filtfilt(b, a, audio)
        return audio + bass * 0.3

    def add_reverb(self, audio: np.ndarray, sr: int, intensity: float = 0.3) -> np.ndarray:
        """添加混响效果"""
        delay_samples = int(0.03 * sr)
        reverb = np.zeros_like(audio)
        reverb[delay_samples:] = audio[:-delay_samples] * intensity
        return audio + reverb

    def auto_enhance(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """AI自动增强"""
        rms = np.sqrt(np.mean(audio**2))

        if rms < 0.1:
            audio = audio * 1.5

        audio = self.adaptive_eq(audio, sr)
        audio = self.add_reverb(audio, sr, 0.2)

        return audio

    def adaptive_eq(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """自适应均衡"""
        freqs = np.fft.rfftfreq(len(audio), 1/sr)
        fft = np.fft.rfft(audio)

        magnitude = np.abs(fft)
        low_energy = np.mean(magnitude[freqs < 500])
        mid_energy = np.mean(magnitude[(freqs >= 500) & (freqs < 2000)])
        high_energy = np.mean(magnitude[freqs >= 2000])

        if low_energy < mid_energy * 0.5:
            audio = self.enhance_bass(audio, sr)

        if high_energy < mid_energy * 0.3:
            b, a = signal.butter(2, 3000 / (sr / 2), 'high')
            highs = signal.filtfilt(b, a, audio)
            audio = audio + highs * 0.2

        return audio

    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """音频归一化"""
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val * 0.95
        return audio
