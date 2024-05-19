# Set PyPI credentials as environment variables

export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-token-something

# Step 1: Build Source Distribution

python setup.py sdist

# Step 2: Build Wheel Distribution (Optional)

python setup.py sdist bdist_wheel

# Step 3: Upload to PyPI (for first push)

twine upload dist/*

# Alternative Upload Command (Skip Existing for new version patching)

twine upload --skip-existing dist/*
