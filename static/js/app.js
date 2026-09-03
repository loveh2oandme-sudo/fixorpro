// FixOrPro - Client Application Logic with 3 Major US Hardware Stores

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
    const loadingStepMsg = document.getElementById("loadingStepMsg");
    const reportContainer = document.getElementById("reportContainer");
    const toastContainer = document.getElementById("toastContainer");
    
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
    
    // Pro Referral Buttons
    const thumbtackBtn = document.getElementById("thumbtackBtn");
    const angiBtn = document.getElementById("angiBtn");
    const yelpBtn = document.getElementById("yelpBtn");
    
    // Actions
    const printReportBtn = document.getElementById("printReportBtn");
    const shareReportBtn = document.getElementById("shareReportBtn");
    const newDiagnosticBtn = document.getElementById("newDiagnosticBtn");

    let currentFile = null;
    let selectedSampleId = null;
    let scanInterval = null;

    // Use saved Amazon tag from localStorage if entered, or fallback
    const AMAZON_TAG = localStorage.getItem("fixorpro_amazon_tag") || "fixorpro-20";

    // Initial load: Fetch samples
    loadSamples();

    // ----------------------------------------------------------------------
    // Toast Notification System
    // ----------------------------------------------------------------------
    function showToast(message) {
        if (!toastContainer) return;
        const toast = document.createElement("div");
        toast.className = "toast";
        toast.textContent = message;
        toastContainer.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = "0";
            toast.style.transform = "translateX(100%)";
            toast.style.transition = "all 0.3s ease";
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // ----------------------------------------------------------------------
    // File Upload & Camera Handlers
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
            showToast("⚠️ Please select an image file (JPG, PNG, WebP).");
            return;
        }

        currentFile = file;
        selectedSampleId = null;
        clearActiveSampleCards();

        const reader = new FileReader();
        reader.onload = (e) => {
            previewThumb.src = e.target.result;
            previewFilename.textContent = `TARGET: ${file.name.toUpperCase()}`;
            const sizeInKb = Math.round(file.size / 1024);
            previewMeta.textContent = `OPTICAL MATRIX LOCKED • ${sizeInKb} KB • READY FOR AI DIAGNOSIS`;

            dropZone.style.display = "none";
            previewContainer.style.display = "block";
            analyzeBtn.disabled = false;
            showToast("📷 Image locked. Ready for AI Analysis!");
        };
        reader.readAsDataURL(file);
    }

    // ----------------------------------------------------------------------
    // Samples Logic with 3D Tilt
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

            // 3D Tilt Effect on mouse move
            card.addEventListener("mousemove", (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left - rect.width / 2;
                const y = e.clientY - rect.top - rect.height / 2;
                card.style.transform = `perspective(600px) rotateX(${-y / 15}deg) rotateY(${x / 15}deg) translateY(-4px)`;
            });

            card.addEventListener("mouseleave", () => {
                card.style.transform = "";
            });

            card.addEventListener("click", () => {
                selectSample(sample);
            });

            sampleCardsContainer.appendChild(card);
        });
    }

    function selectSample(sample) {
        selectedSampleId = sample.id;
        currentFile = null;

        clearActiveSampleCards();
        const activeCard = document.querySelector(`.sample-card[data-id="${sample.id}"]`);
        if (activeCard) activeCard.classList.add("active");

        previewThumb.src = sample.image_url;
        previewFilename.textContent = `TARGET: ${sample.title.toUpperCase()}`;
        previewMeta.textContent = `${sample.category.toUpperCase()} • INSTANT DEMO SCENARIO`;

        dropZone.style.display = "none";
        previewContainer.style.display = "block";
        userNotesInput.value = sample.description || "";
        analyzeBtn.disabled = false;

        runDiagnosis();
    }

    function clearActiveSampleCards() {
        document.querySelectorAll(".sample-card").forEach(c => c.classList.remove("active"));
    }

    // ----------------------------------------------------------------------
    // Diagnosis Execution & Progress Animation
    // ----------------------------------------------------------------------
    analyzeBtn.addEventListener("click", runDiagnosis);

    async function runDiagnosis() {
        if (!currentFile && !selectedSampleId) {
            showToast("⚠️ Please upload a photo or pick a sample scenario.");
            return;
        }

        // Show loading HUD
        reportContainer.style.display = "none";
        loadingBox.style.display = "block";
        analyzeBtn.disabled = true;
        loadingBox.scrollIntoView({ behavior: "smooth", block: "center" });

        // Cycle Scanning Messages
        const scanSteps = [
            "[1/4] Scanning surface defect vectors...",
            "[2/4] Cross-referencing US National Building & Plumbing Codes...",
            "[3/4] Querying Amazon, Home Depot & Lowe's parts pricing...",
            "[4/4] Generating final actionable repair blueprint..."
        ];
        let stepIdx = 0;
        loadingStepMsg.textContent = scanSteps[0];
        clearInterval(scanInterval);
        scanInterval = setInterval(() => {
            stepIdx = (stepIdx + 1) % scanSteps.length;
            loadingStepMsg.textContent = scanSteps[stepIdx];
        }, 900);

        const formData = new FormData();
        if (currentFile) formData.append("image", currentFile);
        if (selectedSampleId) formData.append("sample_id", selectedSampleId);

        const notes = userNotesInput.value.trim();
        if (notes) formData.append("notes", notes);

        const savedKey = localStorage.getItem("fixorpro_gemini_key");
        if (savedKey) formData.append("api_key", savedKey);

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
            clearInterval(scanInterval);
            renderDiagnosticReport(data.data, data.source);
            showToast("✨ AI Diagnostic Scan Complete!");

        } catch (err) {
            console.error("Diagnosis error:", err);
            showToast("❌ Diagnostic Error: " + err.message);
        } finally {
            clearInterval(scanInterval);
            loadingBox.style.display = "none";
            analyzeBtn.disabled = false;
        }
    }

    // ----------------------------------------------------------------------
    // Render Result Report (Amazon + Home Depot + Lowe's)
    // ----------------------------------------------------------------------
    function renderDiagnosticReport(data, source) {
        const isDIY = data.verdict === "DIY_RECOMMENDED";

        // 1. Verdict Banner
        verdictBanner.className = `verdict-banner ${isDIY ? 'diy' : 'pro'}`;
        verdictIcon.textContent = isDIY ? "🟢" : "🚨";
        verdictTag.textContent = isDIY ? "DIY Recommended (Beginner Friendly)" : "Call a Licensed Contractor";
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
        specConfidence.textContent = data.confidence_score || "High (95%)";

        // YouTube Main Video Guide Button
        const youtubeMainBtn = document.getElementById("youtubeMainBtn");
        if (youtubeMainBtn) {
            const ytQuery = data.youtube_query || `${data.problem_title} DIY repair tutorial`;
            youtubeMainBtn.href = `https://www.youtube.com/results?search_query=${encodeURIComponent(ytQuery)}`;
        }

        // 4. Interactive Deep Step-by-Step Manual
        stepsListContainer.innerHTML = "";
        if (data.steps && data.steps.length > 0) {
            data.steps.forEach(step => {
                const stepEl = document.createElement("div");
                stepEl.className = "step-item";

                let proTipHtml = "";
                if (step.pro_tip) {
                    proTipHtml = `<div class="step-protip-box">💡 <strong>Pro Tip:</strong> ${step.pro_tip}</div>`;
                }

                let cautionHtml = "";
                if (step.caution) {
                    cautionHtml = `<div class="step-caution-box">⚠️ <strong>Watch Out:</strong> ${step.caution}</div>`;
                }

                let stepYtHtml = "";
                if (step.youtube_query) {
                    stepYtHtml = `
                        <div>
                            <a href="https://www.youtube.com/results?search_query=${encodeURIComponent(step.youtube_query)}" target="_blank" rel="noopener noreferrer" class="step-video-link" onclick="event.stopPropagation();">
                                <span>▶️ Watch Step Demo on YouTube</span>
                            </a>
                        </div>
                    `;
                }

                stepEl.innerHTML = `
                    <div class="step-checkbox-wrap">✓</div>
                    <div class="step-info">
                        <h4>Step ${step.step_num}: ${step.title}</h4>
                        <p class="step-instruction-text">${step.instruction}</p>
                        ${proTipHtml}
                        ${cautionHtml}
                        ${stepYtHtml}
                    </div>
                `;

                // Interactive Step Toggle
                stepEl.addEventListener("click", () => {
                    stepEl.classList.toggle("completed");
                    if (stepEl.classList.contains("completed")) {
                        showToast(`Step ${step.step_num} marked as completed!`);
                    }
                });

                stepsListContainer.appendChild(stepEl);
            });
        }

        // Sanitizer helper for retail store queries (removes slashes, parentheses, and invalid characters)
        function sanitizeRetailQuery(str) {
            if (!str) return "home repair";
            return str
                .replace(/\(.*?\)/g, " ")      // remove parentheses and contents (e.g. (or 3-inch))
                .replace(/[\\/]/g, " ")        // remove slashes (prevents Home Depot 404 path errors)
                .replace(/["'#&%$@!+]/g, " ")  // remove special chars
                .replace(/\s+/g, " ")          // collapse spaces
                .trim();
        }

        // 5. Section 1: Materials & Tools with 3 Top US Retailers
        materialsContainer.innerHTML = "";
        if (data.materials_needed && data.materials_needed.length > 0) {
            data.materials_needed.forEach(mat => {
                const cleanQuery = sanitizeRetailQuery(mat.homedepot_search || mat.amazon_search || mat.name);
                const amzUrl = `https://www.amazon.com/s?k=${encodeURIComponent(mat.amazon_search || cleanQuery)}&tag=${AMAZON_TAG}`;
                const hdUrl = `https://www.homedepot.com/s/${encodeURIComponent(cleanQuery)}`;
                const lowesUrl = `https://www.lowes.com/search?searchTerm=${encodeURIComponent(cleanQuery)}`;
                
                const matEl = document.createElement("div");
                matEl.className = "item-card";
                matEl.innerHTML = `
                    <div>
                        <div class="item-name">${mat.name}</div>
                        <div class="item-price">Est. ${mat.est_price || '$5-$20'}</div>
                    </div>
                    <div class="item-links">
                        <a href="${amzUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-amazon">📦 Buy on Amazon</a>
                        <a href="${hdUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-homedepot">🔨 Pick up at Home Depot Today</a>
                        <a href="${lowesUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-lowes">🏠 Lowe's Store / Ship</a>
                    </div>
                `;
                materialsContainer.appendChild(matEl);
            });
        }

        toolsContainer.innerHTML = "";
        if (data.tools_needed && data.tools_needed.length > 0) {
            data.tools_needed.forEach(tool => {
                const cleanQuery = sanitizeRetailQuery(tool.homedepot_search || tool.amazon_search || tool.name);
                const amzUrl = `https://www.amazon.com/s?k=${encodeURIComponent(tool.amazon_search || cleanQuery)}&tag=${AMAZON_TAG}`;
                const hdUrl = `https://www.homedepot.com/s/${encodeURIComponent(cleanQuery)}`;
                const lowesUrl = `https://www.lowes.com/search?searchTerm=${encodeURIComponent(cleanQuery)}`;
                
                const toolEl = document.createElement("div");
                toolEl.className = "item-card";
                toolEl.innerHTML = `
                    <div class="item-name">🛠️ ${tool.name}</div>
                    <div class="item-links">
                        <a href="${amzUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-amazon">📦 Buy on Amazon</a>
                        <a href="${hdUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-homedepot">🔨 Home Depot</a>
                        <a href="${lowesUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-lowes">🏠 Lowe's</a>
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
        
        // Accurate smooth scroll with header clearance
        setTimeout(() => {
            const header = document.querySelector(".site-header");
            const headerHeight = header ? header.offsetHeight + 20 : 90;
            const targetPos = reportContainer.getBoundingClientRect().top + window.pageYOffset - headerHeight;
            window.scrollTo({
                top: Math.max(0, targetPos),
                behavior: "smooth"
            });
        }, 100);
    }


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
            showToast("🔗 Report link copied to clipboard!");
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
});
