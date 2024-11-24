import os
import subprocess


def build_game():
    # Get absolute path of assets folders
    current_dir = os.path.dirname(os.path.abspath(__file__))
    space_shooter_dir = os.path.join(current_dir, 'space shooter')
    audio_path = os.path.join(space_shooter_dir, 'audio')
    image_path = os.path.join(space_shooter_dir, 'images')

    # Simple command - just use the spec file
    cmd = [
        'pyinstaller',
        'main.spec'
    ]

    print("Building with command:", ' '.join(cmd))
    print(f"Current directory: {current_dir}")
    print(f"Space shooter directory: {space_shooter_dir}")
    print(f"Audio path: {audio_path}")
    print(f"Image path: {image_path}")

    # Run the build command
    try:
        subprocess.run(cmd, check=True)
        print("Build completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Build failed with error: {e}")


if __name__ == "__main__":
    build_game()
