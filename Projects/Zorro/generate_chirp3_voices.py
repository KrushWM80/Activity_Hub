"""
Google Cloud Vertex AI Chirp 3 HD Voice Generator
Generates high-quality audio using Google Cloud's Chirp 3 HD voices
"""

import os
import json
from pathlib import Path
from google.cloud import texttospeech

# Configuration
OUTPUT_DIR = Path("Store Support/Projects/AMP/Zorro/output/podcasts")
MESSAGE_BODY = """
Welcome to your weekly message update! 

This is your message from the Activity Hub. We have some important updates to share with you this week.

FOOD AND CONSUMABLES:
Your team has been doing an excellent job in the food and consumables department. We've seen strong performance across all product categories. Make sure to maintain your focus on freshness and proper rotation. Customer feedback has been very positive about product quality and availability. Keep up the great work and continue to prioritize the store experience for our shoppers.

GENERAL MERCHANDISE:
General merchandise is showing solid growth this week. We appreciate your attention to detail with pricing accuracy and planogram compliance. The new layout implementation has been well-received by customers. Make sure all team members understand the new organization system. Cleanliness and presentation standards continue to be important - thank you for maintaining those high standards.

OPERATIONS:
Operational efficiency has been excellent this week. Staffing levels are appropriate, and scheduling is working well. We've noticed some great improvements in processing times. Keep communicating any challenges early so we can address them together. Your dedication to operational excellence is making a real difference.

Thank you for your continued commitment and hard work. We'll have more updates for you next week. Keep it up!
"""

CHIRP3_VOICES = {
    "achird": {
        "language_code": "en-US",
        "name": "en-US-Chirp3-HD-Achird",
        "gender": "Male"
    },
    "bemrose": {
        "language_code": "en-US", 
        "name": "en-US-Chirp3-HD-Bemrose",
        "gender": "Female"
    }
}

class Chirp3VoiceGenerator:
    """Generate audio using Google Cloud Vertex AI Chirp 3 HD Voices"""
    
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()
        self.output_dir = OUTPUT_DIR
        self.message_body = MESSAGE_BODY
        
        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_audio(self, voice_key, voice_name):
        """
        Generate audio for a specific Chirp 3 voice
        
        Args:
            voice_key: Key in CHIRP3_VOICES dict (e.g., 'achird', 'bemrose')
            voice_name: Display name (e.g., 'Achird', 'Bemrose')
        
        Returns:
            dict: Result with filename, size, duration info
        """
        voice_config = CHIRP3_VOICES.get(voice_key)
        if not voice_config:
            return {"error": f"Voice '{voice_key}' not found in configuration"}
        
        print(f"\n{'='*60}")
        print(f"Generating Chirp3 HD {voice_name} Voice")
        print(f"{'='*60}")
        
        try:
            # Build synthesis input
            synthesis_input = texttospeech.SynthesisInput(text=self.message_body)
            
            # Build voice configuration
            voice = texttospeech.VoiceSelectionParams(
                language_code=voice_config["language_code"],
                name=voice_config["name"]
            )
            
            # Build audio configuration for MP3 output
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.0,  # Normal speed
                pitch=0.0,           # Normal pitch
                volume_gain_db=2.0   # Slightly louder for clarity
            )
            
            print(f"Voice: {voice_config['name']}")
            print(f"Gender: {voice_config['gender']}")
            print(f"Language: {voice_config['language_code']}")
            print(f"Audio Format: MP3 (HD Quality)")
            print("\nGenerating audio... ", end="", flush=True)
            
            # Request synthesis
            request = texttospeech.SynthesizeSpeechRequest(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            response = self.client.synthesize_speech(request=request)
            
            # Save to file
            filename = f"Your Week 4 Messages are Here - Audio - Reading - Chirp3 {voice_name}.mp3"
            filepath = self.output_dir / filename
            
            with open(filepath, "wb") as f:
                f.write(response.audio_content)
            
            file_size_mb = filepath.stat().st_size / 1024 / 1024
            
            print("✅ Complete")
            print(f"\nFile Details:")
            print(f"  Name: {filename}")
            print(f"  Size: {file_size_mb:.2f} MB")
            print(f"  Path: {filepath}")
            print(f"  Encoding: MP3 (HD Quality, 24kHz)")
            
            return {
                "success": True,
                "filename": filename,
                "filepath": str(filepath),
                "size_mb": round(file_size_mb, 2),
                "voice": voice_key,
                "voice_name": voice_name,
                "encoding": "MP3"
            }
            
        except Exception as e:
            error_msg = f"Error generating {voice_name} voice: {str(e)}"
            print(f"❌ Failed: {error_msg}")
            return {"error": error_msg}
    
    def generate_all_chirp3_voices(self):
        """Generate audio for all available Chirp 3 voices"""
        print("\n" + "="*60)
        print("CHIRP 3 HD VOICE GENERATION")
        print("="*60)
        print("\nAvailable voices:", ", ".join([f"{v} ({CHIRP3_VOICES[v]['gender']})" 
                                               for v in CHIRP3_VOICES.keys()]))
        
        results = []
        for voice_key in CHIRP3_VOICES.keys():
            voice_name = voice_key.capitalize()
            result = self.generate_audio(voice_key, voice_name)
            results.append(result)
        
        # Summary
        print("\n" + "="*60)
        print("GENERATION SUMMARY")
        print("="*60)
        successful = [r for r in results if r.get("success")]
        failed = [r for r in results if not r.get("success")]
        
        print(f"\n✅ Successful: {len(successful)}/{len(results)}")
        for result in successful:
            print(f"   • {result['filename']} ({result['size_mb']} MB)")
        
        if failed:
            print(f"\n❌ Failed: {len(failed)}/{len(results)}")
            for result in failed:
                print(f"   • {result.get('error', 'Unknown error')}")
        
        print(f"\nOutput directory: {self.output_dir}")
        print("="*60)
        
        return results


def main():
    """Main execution"""
    print("\n" + "="*60)
    print("GOOGLE CLOUD VERTEX AI - CHIRP 3 HD VOICE GENERATOR")
    print("="*60)
    
    # Check for credentials
    if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
        print("\n❌ ERROR: Google Cloud credentials not configured")
        print("\nTo set up Google Cloud Vertex AI Chirp 3 voices:")
        print("1. Create a Google Cloud project")
        print("2. Enable the Text-to-Speech API")
        print("3. Create a service account JSON key")
        print("4. Set GOOGLE_APPLICATION_CREDENTIALS environment variable:")
        print("   set GOOGLE_APPLICATION_CREDENTIALS=path\\to\\credentials.json")
        print("\nSee CHIRP3_SETUP_GUIDE.md for detailed instructions")
        return
    
    # Generate voices
    generator = Chirp3VoiceGenerator()
    results = generator.generate_all_chirp3_voices()
    
    # Return status
    successful = len([r for r in results if r.get("success")])
    if successful == len(results):
        print("\n✅ All Chirp 3 voices generated successfully!")
    else:
        print(f"\n⚠️  Generated {successful}/{len(results)} voices")


if __name__ == "__main__":
    main()
