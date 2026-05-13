document.addEventListener("DOMContentLoaded", function () {

    // ─── Ask Form: show spinner on submit ───────────────────────────
    const askForm = document.getElementById("ask-form");
    if (askForm) {
        askForm.addEventListener("submit", function () {
            const btn     = document.getElementById("ask-btn");
            const text    = btn.querySelector(".btn-text");
            const spinner = document.getElementById("spinner");
            if (btn && text && spinner) {
                text.textContent = "Searching...";
                spinner.classList.remove("hidden");
                btn.disabled = true;
            }
        });
    }

    // ─── Upload: drag-and-drop + file preview ───────────────────────
    const dropZone   = document.getElementById("drop-zone");
    const fileInput  = document.getElementById("file");
    const preview    = document.getElementById("file-preview");
    const previewName = document.getElementById("file-preview-name");
    const clearBtn   = document.getElementById("file-clear");

    function showPreview(name) {
        if (!preview || !previewName) return;
        previewName.textContent = name;
        preview.classList.remove("hidden");
        if (dropZone) dropZone.classList.add("hidden");
    }

    function clearFile() {
        if (fileInput)   fileInput.value = "";
        if (preview)     preview.classList.add("hidden");
        if (dropZone)    dropZone.classList.remove("hidden");
    }

    if (fileInput) {
        fileInput.addEventListener("change", function () {
            if (this.files[0]) showPreview(this.files[0].name);
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener("click", clearFile);
    }

    if (dropZone) {
        dropZone.addEventListener("click", function (e) {
            if (e.target.classList.contains("drop-browse") || e.target === dropZone ||
                e.target.classList.contains("drop-text") ||
                e.target.classList.contains("drop-icon") ||
                e.target.classList.contains("drop-hint")) {
                fileInput && fileInput.click();
            }
        });

        dropZone.addEventListener("dragover",  function (e) { e.preventDefault(); dropZone.classList.add("dragover"); });
        dropZone.addEventListener("dragleave", function ()  { dropZone.classList.remove("dragover"); });
        dropZone.addEventListener("drop",      function (e) {
            e.preventDefault();
            dropZone.classList.remove("dragover");
            const file = e.dataTransfer.files[0];
            if (file && file.name.endsWith(".pdf")) {
                const dt = new DataTransfer();
                dt.items.add(file);
                fileInput.files = dt.files;
                showPreview(file.name);
            } else {
                alert("Please drop a PDF file.");
            }
        });
    }

    // ─── Upload form: show spinner ───────────────────────────────────
    const uploadForm = document.getElementById("upload-form");
    if (uploadForm) {
        uploadForm.addEventListener("submit", function () {
            const btn = document.getElementById("upload-btn");
            if (btn) {
                btn.textContent = "Processing...";
                btn.disabled = true;
            }
        });
    }

    // ─── Auto-dismiss flash messages after 4 s ───────────────────────
    document.querySelectorAll(".flash").forEach(function (el) {
        setTimeout(function () {
            el.style.transition = "opacity 0.4s";
            el.style.opacity    = "0";
            setTimeout(function () { el.remove(); }, 400);
        }, 4000);
    });
});
