// ─── Model Switcher ───
const modelSelect = document.getElementById('modelSelect');
const modelLoader = document.getElementById('modelLoader');

async function loadModelList() {
    try {
        const res = await fetch('/api/models');
        const data = await res.json();
        modelSelect.innerHTML = '';
        if (data.models.length === 0) {
            modelSelect.innerHTML = '<option value="">No models found</option>';
            return;
        }
        data.models.forEach(name => {
            const opt = document.createElement('option');
            opt.value = name;
            // Remove .gguf from display for cleaner look
            opt.textContent = name.replace('.gguf', '');
            modelSelect.appendChild(opt);
        });
        // Try to select the currently active one (if known)
        // We'll just select the first one by default.
    } catch {
        modelSelect.innerHTML = '<option value="">Error loading</option>';
    }
}

modelSelect.addEventListener('change', async function() {
    const filename = this.value;
    if (!filename) return;

    modelLoader.style.display = 'inline-block';
    modelSelect.disabled = true;

    try {
        const res = await fetch('/api/switch-model', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename })
        });
        const data = await res.json();
        if (data.success) {
            // Change the badge or just show a brief success
            alert(`✅ Switched to ${filename.replace('.gguf', '')}`);
        } else {
            alert(`❌ Failed: ${data.error}`);
        }
    } catch (err) {
        alert('❌ Could not reach server.');
    } finally {
        modelLoader.style.display = 'none';
        modelSelect.disabled = false;
    }
});

// Load models when page loads
loadModelList();