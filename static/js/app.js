// FixOrPro - Client Application Logic

document.addEventListener("DOMContentLoaded", () => {
    // DOM Elements
    const dropZone = document.getElementById("dropZone");
    const fileInput = document.getElementById("fileInput");
    const cameraInput = document.getElementById("cameraInput");
    const previewContainer = document.getElementById("previewContainer");
    const previewThumb = document.getElementById("previewThumb");
    const previewFilename = document.getElementById("previewFilename");
    const previewMeta = document.getElementById("previewMeta");
    const removeImageBtn = document.getElementById("removeImageBtn");
    const userNotesInput = document.getElementById("userNotes");
    const analyzeBtn = document.getElementById("analyzeBtn");
    
    const sampleCardsContainer = document.getElementById("sampleCardsContainer");
    const loadingBox = document.getElementById("loadingBox");
    const reportContainer = document.getElementById("reportContainer");
    
    // Result Elements
    const verdictBanner = document.getElementById("verdictBanner");
    const verdictIcon = document.getElementById("verdictIcon");
    const verdictTag = document.getElementById("verdictTag");
    const verdictHeading = document.getElementById("verdictHeading");
    const savingsPill = document.getElementById("savingsPill");
    const problemSummary = document.getElementById("problemSummary");
    
    const diyCostVal = document.getElementById("diyCostVal");
    const diyCostDetail = document.getElementById("diyCostDetail");
    const proCostVal = document.getElementById("proCostVal");
    const savingsCostVal = document.getElementById("savingsCostVal");
    
    const specDifficulty = document.getElementById("specDifficulty");
    const specTime = document.getElementById("specTime");
    const specCategory = document.getElementById("specCategory");
    const specConfidence = document.getElementById("specConfidence");
    
    const stepsListContainer = document.getElementById("stepsListContainer");
    const materialsContainer = document.getElementById("materialsContainer");
    const toolsContainer = document.getElementById("toolsContainer");
    const warningsContainer = document.getElementById("warningsContainer");
    const proTriggerBox = document.getElementById("proTriggerBox");
    const proSearchTerm = document.getElementById("proSearchTerm");
    
    // Pro Referral Buttons
    const thumbtackBtn = document.getElementById("thumbtackBtn");
    const angiBtn = document.getElementById("angiBtn");
    const yelpBtn = document.getElementById("yelpBtn");
    
    // Actions
    const printReportBtn = document.getElementById("printReportBtn");
    const shareReportBtn = document.getElementById("shareReportBtn");
    const newDiagnosticBtn = document.getElementById("newDiagnosticBtn");
    
    // Settings Modal
    const apiKeyBtn = document.getElementById("apiKeyBtn");
    const settingsModal = document.getElementById("settingsModal");
    const closeModalBtn = document.getElementById("closeModalBtn");
    const saveKeyBtn = document.getElementById("saveKeyBtn");
    const apiKeyInput = document.getElementById("apiKeyInput");
    const amazonTagInput = document.getElementById("amazonTagInput");
    const keyStatusBadge = document.getElementById("keyStatusBadge");

    let currentFile = null;
    let selectedSampleId = null;

    // Load saved settings
    const savedApiKey = localStorage.getItem("fixorpro_gemini_key") || "";
    const savedAmazonTag = localStorage.getItem("fixorpro_amazon_tag") || "fixorpro-20";
    if (apiKeyInput) apiKeyInput.value = savedApiKey;
    if (amazonTagInput) amazonTagInput.value = savedAmazonTag;
    updateKeyStatusBadge(savedApiKey);

    // Initial load: Fetch samples
    loadSamples();

    // ----------------------------------------------------------------------
    // File Upload & Drag-and-Drop Handlers
    // ----------------------------------------------------------------------
    dropZone.addEventListener("click", () => fileInput.click());

    document.getElementById("btnSelectFile").addEventListener("click", (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    document.getElementById("btnCamera").addEventListener("click", (e) => {
        e.stopPropagation();
        cameraInput.click();
    });

    fileInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFileSelection(e.target.files[0]);
        }
    });

    cameraInput.addEventListener("change", (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFileSelection(e.target.files[0]);
        }
    });

    // Drag & Drop
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('dragover');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('dragover');
        });
    });

    dropZone.addEventListener("drop", (e) => {
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });

    removeImageBtn.addEventListener("click", () => {
        currentFile = null;
        selectedSampleId = null;
        fileInput.value = "";
        cameraInput.value = "";
        previewContainer.style.display = "none";
        dropZone.style.display = "block";
        analyzeBtn.disabled = true;
        clearActiveSampleCards();
    });

    function handleFileSelection(file) {
        if (!file.type.startsWith("image/")) {
            alert("Please select a valid image file (JPG, PNG, WebP, HEIC).");
            return;
        }

        currentFile = file;
        selectedSampleId = null;
        clearActiveSampleCards();

        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            previewThumb.src = e.target.result;
            previewFilename.textContent = file.name;
            const sizeInKb = Math.round(file.size / 1024);
            previewMeta.textContent = `${file.type} • ${sizeInKb} KB`;

            dropZone.style.display = "none";
            previewContainer.style.display = "block";
            analyzeBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }

    // ----------------------------------------------------------------------
    // Samples Logic
    // ----------------------------------------------------------------------
    async function loadSamples() {
        try {
            const res = await fetch("/api/samples");
            const data = await res.json();
            renderSampleCards(data.samples);
        } catch (err) {
            console.error("Failed to load sample scenarios:", err);
        }
    }

    function renderSampleCards(samples) {
        if (!sampleCardsContainer) return;
        sampleCardsContainer.innerHTML = "";

        samples.forEach(sample => {
            const card = document.createElement("div");
            card.className = "sample-card glass-panel";
            card.dataset.id = sample.id;
            card.innerHTML = `
                <div>
                    <div class="sample-thumb-icon">${sample.thumbnail}</div>
                    <div class="sample-name">${sample.title}</div>
                </div>
                <div class="sample-badge">${sample.category}</div>
            `;

            card.addEventListener("click", () => {
                selectSample(sample);
            });

            sampleCardsContainer.appendChild(card);
        });
    }

    function selectSample(sample) {
        selectedSampleId = sample.id;
        currentFile = null;

        // Highlight card
        clearActiveSampleCards();
        const activeCard = document.querySelector(`.sample-card[data-id="${sample.id}"]`);
        if (activeCard) activeCard.classList.add("active");

        // Update preview area with sample image
        previewThumb.src = sample.image_url;
        previewFilename.textContent = sample.title;
        previewMeta.textContent = `${sample.category} • Instant Demo Case`;

        dropZone.style.display = "none";
        previewContainer.style.display = "block";
        userNotesInput.value = sample.description || "";
        analyzeBtn.disabled = false;

        // Automatically trigger diagnosis for fast demo
        runDiagnosis();
    }

    function clearActiveSampleCards() {
        document.querySelectorAll(".sample-card").forEach(c => c.classList.remove("active"));
    }

    // ----------------------------------------------------------------------
    // Diagnosis Execution
    // ----------------------------------------------------------------------
    analyzeBtn.addEventListener("click", runDiagnosis);

    async function runDiagnosis() {
        if (!currentFile && !selectedSampleId) {
            alert("Please upload a photo or pick a sample scenario.");
            return;
        }

        // Show loading state
        reportContainer.style.display = "none";
        loadingBox.style.display = "block";
        analyzeBtn.disabled = true;
        loadingBox.scrollIntoView({ behavior: "smooth", block: "center" });

        const formData = new FormData();
        if (currentFile) {
            formData.append("image", currentFile);
        }
        if (selectedSampleId) {
            formData.append("sample_id", selectedSampleId);
        }

        const notes = userNotesInput.value.trim();
        if (notes) {
            formData.append("notes", notes);
        }

        const savedKey = localStorage.getItem("fixorpro_gemini_key");
        if (savedKey) {
            formData.append("api_key", savedKey);
        }

        try {
            const res = await fetch("/api/analyze", {
                method: "POST",
                body: formData
            });

            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.detail || "Failed to analyze image.");
            }

            const data = await res.json();
            renderDiagnosticReport(data.data, data.source);

        } catch (err) {
            console.error("Diagnosis error:", err);
            alert("Diagnostic error: " + err.message);
        } finally {
            loadingBox.style.display = "none";
            analyzeBtn.disabled = false;
        }
    }

    // ----------------------------------------------------------------------
    // Render Result Report
    // ----------------------------------------------------------------------
    function renderDiagnosticReport(data, source) {
        const isDIY = data.verdict === "DIY_RECOMMENDED";
        const amazonTag = localStorage.getItem("fixorpro_amazon_tag") || "fixorpro-20";

        // 1. Verdict Banner
        verdictBanner.className = `verdict-banner ${isDIY ? 'diy' : 'pro'}`;
        verdictIcon.textContent = isDIY ? "🟢" : "🚨";
        verdictTag.textContent = isDIY ? "DIY Recommended" : "Call a Licensed Pro";
        verdictHeading.textContent = data.problem_title;
        problemSummary.textContent = data.summary;

        // Savings Ribbon
        const savingsText = data.cost_comparison?.estimated_savings || "$0";
        if (isDIY && savingsText !== "$0") {
            savingsPill.style.display = "flex";
            savingsPill.innerHTML = `<span>💰 Save ~${savingsText}</span>`;
        } else {
            savingsPill.style.display = "none";
        }

        // 2. Cost Cards
        diyCostVal.textContent = data.cost_comparison?.diy_cost || "$0";
        proCostVal.textContent = data.cost_comparison?.pro_cost || "$150+";
        savingsCostVal.textContent = isDIY ? savingsText : "$0 (Pro Required)";

        // 3. Quick Specs Strip
        specDifficulty.textContent = data.difficulty || "Beginner";
        specTime.textContent = data.estimated_time || "20 mins";
        specCategory.textContent = data.category || "General Repair";
        specConfidence.textContent = data.confidence_score || "High";

        // 4. Tab 1: Steps
        stepsListContainer.innerHTML = "";
        if (data.steps && data.steps.length > 0) {
            data.steps.forEach(step => {
                const stepEl = document.createElement("div");
                stepEl.className = "step-item";
                stepEl.innerHTML = `
                    <div class="step-number">${step.step_num}</div>
                    <div class="step-info">
                        <h4>${step.title}</h4>
                        <p>${step.instruction}</p>
                    </div>
                `;
                stepsListContainer.appendChild(stepEl);
            });
        }

        // 5. Tab 2: Materials & Tools
        materialsContainer.innerHTML = "";
        if (data.materials_needed && data.materials_needed.length > 0) {
            data.materials_needed.forEach(mat => {
                const amzUrl = `https://www.amazon.com/s?k=${encodeURIComponent(mat.amazon_search || mat.name)}&tag=${amazonTag}`;
                const hdUrl = `https://www.homedepot.com/s/${encodeURIComponent(mat.homedepot_search || mat.name)}`;
                
                const matEl = document.createElement("div");
                matEl.className = "item-card";
                matEl.innerHTML = `
                    <div>
                        <div class="item-name">${mat.name}</div>
                        <div class="item-price">Est. ${mat.est_price || '$5-$20'}</div>
                    </div>
                    <div class="item-links">
                        <a href="${amzUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-amazon">📦 Amazon</a>
                        <a href="${hdUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-homedepot">🔨 Home Depot</a>
                    </div>
                `;
                materialsContainer.appendChild(matEl);
            });
        }

        toolsContainer.innerHTML = "";
        if (data.tools_needed && data.tools_needed.length > 0) {
            data.tools_needed.forEach(tool => {
                const amzUrl = `https://www.amazon.com/s?k=${encodeURIComponent(tool.amazon_search || tool.name)}&tag=${amazonTag}`;
                const hdUrl = `https://www.homedepot.com/s/${encodeURIComponent(tool.homedepot_search || tool.name)}`;
                
                const toolEl = document.createElement("div");
                toolEl.className = "item-card";
                toolEl.innerHTML = `
                    <div class="item-name">🛠️ ${tool.name}</div>
                    <div class="item-links">
                        <a href="${amzUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-amazon">Buy on Amazon</a>
                        <a href="${hdUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-homedepot">Home Depot</a>
                    </div>
                `;
                toolsContainer.appendChild(toolEl);
            });
        }

        // 6. Tab 3: Safety Warnings
        warningsContainer.innerHTML = "";
        if (data.safety_warnings && data.safety_warnings.length > 0) {
            const ul = document.createElement("ul");
            ul.className = "warning-list";
            data.safety_warnings.forEach(w => {
                const li = document.createElement("li");
                li.textContent = w;
                ul.appendChild(li);
            });
            warningsContainer.appendChild(ul);
        }

        if (data.pro_trigger_conditions) {
            proTriggerBox.textContent = data.pro_trigger_conditions;
        }

        // 7. Pro Referral Links
        const queryTerm = encodeURIComponent(data.category || data.problem_title || "Handyman");
        thumbtackBtn.href = `https://www.thumbtack.com/k/${queryTerm}/near-me`;
        angiBtn.href = `https://www.angi.com/companylist/${queryTerm}.htm`;
        yelpBtn.href = `https://www.yelp.com/search?find_desc=${queryTerm}`;

        // Reveal Report
        reportContainer.style.display = "block";
        reportContainer.scrollIntoView({ behavior: "smooth", block: "start" });
    }

    // ----------------------------------------------------------------------
    // Tabs Navigation
    // ----------------------------------------------------------------------
    document.querySelectorAll(".tab-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const targetTab = btn.dataset.tab;

            document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));

            btn.classList.add("active");
            const content = document.getElementById(targetTab);
            if (content) content.classList.add("active");
        });
    });

    // ----------------------------------------------------------------------
    // Actions: Print, Share, New Diagnosis
    // ----------------------------------------------------------------------
    printReportBtn.addEventListener("click", () => {
        window.print();
    });

    shareReportBtn.addEventListener("click", () => {
        if (navigator.share) {
            navigator.share({
                title: 'FixOrPro Diagnostic Report',
                text: 'Check out this home repair diagnostic report generated by FixOrPro AI!',
                url: window.location.href,
            }).catch(() => {});
        } else {
            navigator.clipboard.writeText(window.location.href);
            alert("Link copied to clipboard! You can share this with family or your contractor.");
        }
    });

    newDiagnosticBtn.addEventListener("click", () => {
        currentFile = null;
        selectedSampleId = null;
        fileInput.value = "";
        cameraInput.value = "";
        userNotesInput.value = "";
        previewContainer.style.display = "none";
        dropZone.style.display = "block";
        reportContainer.style.display = "none";
        clearActiveSampleCards();
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    // ----------------------------------------------------------------------
    // API Key & Settings Modal
    // ----------------------------------------------------------------------
    apiKeyBtn.addEventListener("click", () => {
        settingsModal.style.display = "flex";
    });

    closeModalBtn.addEventListener("click", () => {
        settingsModal.style.display = "none";
    });

    settingsModal.addEventListener("click", (e) => {
        if (e.target === settingsModal) {
            settingsModal.style.display = "none";
        }
    });

    saveKeyBtn.addEventListener("click", () => {
        const key = apiKeyInput.value.trim();
        const tag = amazonTagInput.value.trim() || "fixorpro-20";

        localStorage.setItem("fixorpro_gemini_key", key);
        localStorage.setItem("fixorpro_amazon_tag", tag);

        updateKeyStatusBadge(key);
        settingsModal.style.display = "none";
        alert("Settings saved successfully!");
    });

    function updateKeyStatusBadge(key) {
        if (key && key.length > 5) {
            keyStatusBadge.textContent = "⚡ Live AI Active";
            keyStatusBadge.style.color = "#34d399";
        } else {
            keyStatusBadge.textContent = "⚙️ Free Demo Mode";
            keyStatusBadge.style.color = "#93c5fd";
        }
    }
});
