# Download Models and Dependencies - Off Walmart Network

## Step 1: Disconnect from VPN
1. Disconnect from Walmart VPN
2. Connect to home network or mobile hotspot
3. Verify internet access: `ping huggingface.co`

---

## Step 2: Install/Update Core Dependencies

```powershell
# Navigate to project directory
cd "c:\Users\hrisaac\OneDrive - Walmart Inc\Documents\VSCode\Projects\zorro"

# Update pip
python -m pip install --upgrade pip

# Install/update all requirements
pip install -r requirements.txt --upgrade

# Install specific AI/ML packages that might need updates
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install diffusers transformers accelerate
pip install huggingface-hub
```

---

## Step 3: Download ModelScope Video Generation Model

### Option A: Using Python (Recommended)
```powershell
# Run this Python script to download the model
python -c "from diffusers import DiffusionPipeline; import torch; print('Downloading ModelScope model...'); pipe = DiffusionPipeline.from_pretrained('damo-vilab/text-to-video-ms-1.7b', torch_dtype=torch.float16, variant='fp16'); print('Download complete!'); print(f'Model cached at: {pipe.config._name_or_path}')"
```

### Option B: Using huggingface-cli
```powershell
# Install CLI if not already installed
pip install huggingface-hub[cli]

# Download the model
huggingface-cli download damo-vilab/text-to-video-ms-1.7b --local-dir C:\Users\hrisaac\.cache\huggingface\hub\models--damo-vilab--text-to-video-ms-1.7b
```

### Option C: Manual Download Script
Save this as `download_model.py` and run it:

```python
"""Download ModelScope text-to-video model."""
import torch
from diffusers import DiffusionPipeline
import os

print("=" * 60)
print("ModelScope Model Downloader")
print("=" * 60)
print()

model_name = "damo-vilab/text-to-video-ms-1.7b"
print(f"Downloading: {model_name}")
print("This may take 10-30 minutes depending on your connection...")
print()

try:
    # Determine device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    
    # Download with progress
    if device == "cuda":
        pipe = DiffusionPipeline.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            variant="fp16"
        )
    else:
        pipe = DiffusionPipeline.from_pretrained(
            model_name,
            torch_dtype=torch.float32
        )
    
    print()
    print("✅ Download complete!")
    print(f"Model cached at: {os.path.expanduser('~/.cache/huggingface')}")
    print()
    print("You can now reconnect to Walmart VPN and use the GUI!")
    
except Exception as e:
    print()
    print(f"❌ Download failed: {e}")
    print()
    print("Troubleshooting:")
    print("1. Check internet connection")
    print("2. Ensure you have ~15GB free disk space")
    print("3. Try again with: pip install --upgrade diffusers transformers")

```

Then run:
```powershell
python download_model.py
```

---

## Step 4: Verify Model Cache

```powershell
# Check if model is cached
python -c "import os; cache_dir = os.path.expanduser('~/.cache/huggingface/hub'); print(f'Cache directory: {cache_dir}'); import os; models = [d for d in os.listdir(cache_dir) if 'damo-vilab' in d.lower()] if os.path.exists(cache_dir) else []; print(f'ModelScope models found: {len(models)}'); [print(f'  - {m}') for m in models]"
```

---

## Step 5: Download Additional Models (Optional)

### OpenAI Whisper (for audio processing)
```powershell
pip install openai-whisper
python -c "import whisper; whisper.load_model('base')"
```

### Download NLTK data (for text processing)
```powershell
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

---

## Step 6: Test Installation

```powershell
# Quick test to verify everything works
python -c "
import torch
from diffusers import DiffusionPipeline
import sys

print('Testing installation...')
print(f'Python: {sys.version}')
print(f'PyTorch: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')

try:
    # Try to load the model (won't generate, just verify it loads)
    print('Loading ModelScope model...')
    pipe = DiffusionPipeline.from_pretrained(
        'damo-vilab/text-to-video-ms-1.7b',
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        variant='fp16' if torch.cuda.is_available() else None
    )
    print('✅ Model loaded successfully!')
    print('Installation complete - ready to use!')
except Exception as e:
    print(f'❌ Error: {e}')
    print('Model may not be fully downloaded.')
"
```

---

## Step 7: Reconnect to Walmart Network

1. Once downloads are complete, reconnect to Walmart VPN
2. The models are now cached locally and won't require internet access
3. Launch the GUI: `python run_gui.py`
4. Generate videos! 🎬

---

## Expected Download Sizes

| Component | Size | Time (50 Mbps) |
|-----------|------|----------------|
| ModelScope Model | ~6-8 GB | 15-25 min |
| PyTorch (CUDA) | ~2-3 GB | 5-10 min |
| Transformers/Diffusers | ~500 MB | 2-3 min |
| **Total** | **~8-12 GB** | **20-40 min** |

---

## Troubleshooting

### "No space left on device"
```powershell
# Check available space
Get-PSDrive C | Select-Object Used,Free
```
Need at least 15GB free for safe installation.

### "CUDA out of memory"
The model will automatically fall back to CPU if GPU memory is insufficient.

### Download interrupted
```powershell
# Resume download by running the same command again
# HuggingFace automatically resumes from where it left off
```

### Verify what's downloaded
```powershell
# Check cache contents
dir "$env:USERPROFILE\.cache\huggingface\hub" -Recurse | Where-Object {$_.Name -like "*damo-vilab*"}
```

---

## Quick Start Commands (Copy-Paste Ready)

```powershell
# Complete download sequence
cd "c:\Users\hrisaac\OneDrive - Walmart Inc\Documents\VSCode\Projects\zorro"
python -m pip install --upgrade pip
pip install -r requirements.txt --upgrade
python -c "from diffusers import DiffusionPipeline; import torch; print('Downloading...'); pipe = DiffusionPipeline.from_pretrained('damo-vilab/text-to-video-ms-1.7b', torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32, variant='fp16' if torch.cuda.is_available() else None); print('Complete!')"
```

---

## After Download Checklist

- [ ] ModelScope model downloaded (~6-8GB)
- [ ] PyTorch with CUDA installed
- [ ] All requirements.txt packages installed
- [ ] Test script ran successfully
- [ ] Reconnected to Walmart VPN
- [ ] GUI launches without errors
- [ ] Ready to generate videos! 🎉

---

**Estimated Total Time: 30-60 minutes**
**Estimated Total Download: 8-12 GB**

Once complete, you'll be able to use the GUI on Walmart network with all models cached locally!
