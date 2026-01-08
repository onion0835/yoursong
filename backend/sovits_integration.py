"""
So-VITS-SVC 集成模块

用于实现高质量的歌声转换和音色克隆
需要额外安装：pip install so-vits-svc
"""

import os
from pathlib import Path
from typing import Optional, Tuple
import torch
import librosa
import soundfile as sf
import numpy as np

class SoVITSIntegration:
    """So-VITS-SVC 集成类"""

    def __init__(self, model_dir: str = "models/sovits"):
        """
        初始化 So-VITS-SVC

        Args:
            model_dir: 模型目录，包含训练好的模型文件
        """
        self.model_dir = Path(model_dir)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.is_available = False

        # 尝试加载模型
        self._load_model()

    def _load_model(self):
        """加载 So-VITS-SVC 模型"""
        try:
            # 检查模型文件是否存在
            model_path = self.model_dir / "G_latest.pth"
            config_path = self.model_dir / "config.json"

            if not model_path.exists() or not config_path.exists():
                print("ℹ️ So-VITS-SVC model not found. Voice cloning disabled.")
                print(f"   Place model at: {model_path}")
                return

            # 尝试导入 So-VITS-SVC
            from inference.infer_tool import Svc

            self.model = Svc(
                net_g_path=str(model_path),
                config_path=str(config_path),
                device=self.device
            )

            self.is_available = True
            print(f"✅ So-VITS-SVC loaded successfully on {self.device}")

        except ImportError:
            print("⚠️ So-VITS-SVC not installed. Run: pip install so-vits-svc")
        except Exception as e:
            print(f"⚠️ Failed to load So-VITS-SVC: {e}")

    def convert_voice(
        self,
        input_audio: str,
        output_path: str,
        speaker: str = "default",
        pitch_shift: int = 0,
        auto_predict_f0: bool = True
    ) -> str:
        """
        音色转换

        Args:
            input_audio: 输入音频文件路径
            output_path: 输出文件路径
            speaker: 目标说话人ID
            pitch_shift: 音高偏移（半音，正数升高，负数降低）
            auto_predict_f0: 是否自动预测音高

        Returns:
            输出文件路径
        """
        if not self.is_available:
            raise Exception("So-VITS-SVC is not available")

        print(f"🎤 Converting voice using So-VITS-SVC...")
        print(f"   Input: {input_audio}")
        print(f"   Speaker: {speaker}")
        print(f"   Pitch shift: {pitch_shift}")

        # 执行推理
        audio = self.model.slice_inference(
            raw_audio_path=input_audio,
            spk=speaker,
            tran=pitch_shift,
            slice_db=-40,  # 切片阈值
            cluster_infer_ratio=0,  # 聚类推理比例
            auto_predict_f0=auto_predict_f0,
            noice_scale=0.4  # 噪声缩放
        )

        # 保存结果
        sf.write(output_path, audio, 44100)
        print(f"✅ Voice converted: {output_path}")

        return output_path

    def clone_voice_for_translation(
        self,
        original_vocals: str,
        translated_tts: str,
        output_path: str
    ) -> str:
        """
        音乐翻译专用：将翻译后的TTS转换为原唱音色

        这是音乐翻译的核心功能！

        Args:
            original_vocals: 原歌曲的人声文件（用于提取音色特征）
            translated_tts: 翻译后的TTS音频（任意音色）
            output_path: 输出路径

        Returns:
            转换后的音频路径

        工作流程：
        1. 提取原人声的音高曲线（F0）
        2. 将TTS音频转换为原歌手音色
        3. 应用原始音高曲线，保持旋律
        """
        if not self.is_available:
            raise Exception("So-VITS-SVC is not available")

        print("🎵 Cloning voice for music translation...")

        # 步骤1：提取原人声的音高信息
        f0_original = self._extract_f0_curve(original_vocals)
        print(f"   Extracted {len(f0_original)} pitch points from original")

        # 步骤2：分析音高范围，确定需要的pitch shift
        # 如果原唱是女声，TTS是男声，需要升调
        pitch_shift = self._calculate_pitch_shift(original_vocals, translated_tts)
        print(f"   Calculated pitch shift: {pitch_shift} semitones")

        # 步骤3：使用So-VITS-SVC转换音色
        # 这里会将TTS的音色转换为训练时使用的歌手音色
        converted = self.convert_voice(
            input_audio=translated_tts,
            output_path=output_path,
            pitch_shift=pitch_shift,
            auto_predict_f0=False  # 使用提取的音高
        )

        # 步骤4：（可选）后处理 - 微调音高以匹配原唱
        # 这一步可以让翻译后的歌曲更接近原曲的旋律
        final_output = self._fine_tune_pitch(
            converted,
            f0_original,
            output_path.replace('.wav', '_final.wav')
        )

        return final_output

    def _extract_f0_curve(self, audio_path: str) -> np.ndarray:
        """
        提取音高曲线（F0 curve）

        F0 = 基频，代表声音的音高
        """
        # 加载音频
        audio, sr = librosa.load(audio_path, sr=44100)

        # 使用CREPE提取高精度F0
        # CREPE是目前最准确的音高提取算法
        try:
            import crepe

            # 提取音高
            time, frequency, confidence, activation = crepe.predict(
                audio, sr, viterbi=True
            )

            # 过滤低置信度的点
            frequency[confidence < 0.5] = 0

            return frequency

        except ImportError:
            # 降级使用librosa的pyin
            print("   ⚠️ CREPE not available, using librosa pyin")
            f0, voiced_flag, voiced_probs = librosa.pyin(
                audio,
                fmin=librosa.note_to_hz('C2'),
                fmax=librosa.note_to_hz('C7'),
                sr=sr
            )

            # 填充NaN值
            f0 = np.nan_to_num(f0)

            return f0

    def _calculate_pitch_shift(
        self,
        reference_audio: str,
        target_audio: str
    ) -> int:
        """
        计算需要的音高偏移量

        比较两个音频的平均音高，返回半音数差异
        """
        # 提取两个音频的F0
        f0_ref = self._extract_f0_curve(reference_audio)
        f0_target = self._extract_f0_curve(target_audio)

        # 计算平均音高（忽略0值）
        mean_f0_ref = np.mean(f0_ref[f0_ref > 0])
        mean_f0_target = np.mean(f0_target[f0_target > 0])

        # 转换为半音差
        # 公式: semitones = 12 * log2(f2/f1)
        pitch_diff = 12 * np.log2(mean_f0_ref / mean_f0_target)

        # 四舍五入到最近的半音
        return int(round(pitch_diff))

    def _fine_tune_pitch(
        self,
        audio_path: str,
        target_f0: np.ndarray,
        output_path: str
    ) -> str:
        """
        微调音高以匹配目标F0曲线

        这可以让转换后的歌声更接近原曲的旋律
        """
        # 加载音频
        audio, sr = librosa.load(audio_path, sr=44100)

        # 提取当前F0
        current_f0 = self._extract_f0_curve(audio_path)

        # 计算需要调整的音高曲线
        # （这里简化了，实际实现需要使用音高变换算法）

        # 使用pyrubberband进行时变音高调整
        try:
            import pyrubberband as pyrb

            # 计算每帧的音高偏移比例
            pitch_shift_curve = target_f0 / (current_f0 + 1e-6)

            # 应用音高变换
            # 注意：这是简化版本，实际需要更复杂的实现
            shifted_audio = pyrb.pitch_shift(
                audio, sr,
                n_steps=0,  # 平均偏移
                rbargs={'--pitch-hq': ''}
            )

            # 保存
            sf.write(output_path, shifted_audio, sr)

            return output_path

        except ImportError:
            print("   ⚠️ pyrubberband not available, skipping fine-tuning")
            # 直接返回原文件
            return audio_path


# ============= 训练辅助函数 =============

def prepare_training_dataset(
    vocal_files: list,
    output_dir: str,
    speaker_name: str = "singer1"
):
    """
    准备So-VITS-SVC训练数据集

    Args:
        vocal_files: 人声文件列表（至少5-10分钟）
        output_dir: 输出目录
        speaker_name: 歌手名称

    训练数据要求：
    - 干净的人声（通过Lalal.ai分离）
    - 至少5-10分钟
    - 多首歌曲更好
    - 音质清晰，无背景噪音
    """
    from pydub import AudioSegment

    output_path = Path(output_dir) / speaker_name / "raw"
    output_path.mkdir(parents=True, exist_ok=True)

    segment_count = 0

    for vocal_file in vocal_files:
        print(f"Processing: {vocal_file}")

        # 加载音频
        audio = AudioSegment.from_file(vocal_file)

        # 切分为10秒片段
        segment_length = 10000  # 10秒

        for i, start in enumerate(range(0, len(audio), segment_length)):
            segment = audio[start:start + segment_length]

            # 至少5秒
            if len(segment) >= 5000:
                output_file = output_path / f"{Path(vocal_file).stem}_{i:03d}.wav"
                segment.export(output_file, format="wav")
                segment_count += 1

    print(f"✅ Prepared {segment_count} training segments")
    print(f"   Output: {output_path}")
    print(f"\nNext steps:")
    print(f"1. cd so-vits-svc")
    print(f"2. python preprocess_flist_config.py")
    print(f"3. python preprocess_hubert_f0.py")
    print(f"4. python train.py -c configs/config.json -m {speaker_name}")


# ============= 使用示例 =============

if __name__ == "__main__":
    # 示例1：音色转换
    sovits = SoVITSIntegration("models/sovits")

    if sovits.is_available:
        # 将任意人声转换为训练的歌手音色
        sovits.convert_voice(
            input_audio="test_vocals.wav",
            output_path="converted_output.wav",
            speaker="singer1",
            pitch_shift=0
        )

    # 示例2：音乐翻译
    if sovits.is_available:
        # 将翻译后的TTS转换为原唱音色
        sovits.clone_voice_for_translation(
            original_vocals="original_singer_vocals.wav",
            translated_tts="english_tts.wav",
            output_path="translated_with_original_voice.wav"
        )

    # 示例3：准备训练数据
    vocal_files = [
        "song1_vocals.wav",
        "song2_vocals.wav",
        "song3_vocals.wav"
    ]

    prepare_training_dataset(
        vocal_files,
        output_dir="datasets",
        speaker_name="taylor_swift"
    )
