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

        // YouTube In-Page Video Player Modal Setup
        const videoModal = document.getElementById("videoModal");
        const videoFrame = document.getElementById("videoFrame");
        const videoTitleText = document.getElementById("videoTitleText");
        const videoModalBuyLinks = document.getElementById("videoModalBuyLinks");
        const closeVideoBtn = document.getElementById("closeVideoBtn");

        function openVideoModal(title, videoId, query) {
            videoTitleText.textContent = title || "DIY Repair Video Tutorial";
            
            // Generate embedded YouTube URL
            let embedUrl = "";
            if (videoId) {
                embedUrl = `https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1&rel=0`;
            } else {
                embedUrl = `https://www.youtube-nocookie.com/embed?listType=search&list=${encodeURIComponent(query || title)}&autoplay=1&rel=0`;
            }
            videoFrame.src = embedUrl;

            // Populate Buy Bar inside Video Modal
            if (videoModalBuyLinks && data.materials_needed && data.materials_needed.length > 0) {
                videoModalBuyLinks.innerHTML = "";
                data.materials_needed.forEach(mat => {
                    const cleanQuery = sanitizeRetailQuery(mat.homedepot_search || mat.amazon_search || mat.name);
                    const amzUrl = `https://www.amazon.com/s?k=${encodeURIComponent(mat.amazon_search || cleanQuery)}&tag=${AMAZON_TAG}`;
                    const hdUrl = `https://www.homedepot.com/s/${encodeURIComponent(cleanQuery)}`;
                    const lowesUrl = `https://www.lowes.com/search?searchTerm=${encodeURIComponent(cleanQuery)}`;
                    
                    const btnWrap = document.createElement("div");
                    btnWrap.style.marginBottom = "8px";
                    btnWrap.innerHTML = `
                        <span style="font-size: 0.85rem; color: #cbd5e1; margin-right: 8px;">• ${mat.name}:</span>
                        <a href="${amzUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-amazon" style="font-size: 0.75rem; padding: 4px 8px;">${SVG_AMAZON} Amazon</a>
                        <a href="${hdUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-homedepot" style="font-size: 0.75rem; padding: 4px 8px;">${SVG_HOMEDEPOT} Home Depot</a>
                        <a href="${lowesUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-lowes" style="font-size: 0.75rem; padding: 4px 8px;">${SVG_LOWES} Lowe's</a>
                    `;
                    videoModalBuyLinks.appendChild(btnWrap);
                });
            }

            videoModal.style.display = "flex";
            document.body.style.overflow = "hidden"; // prevent background scroll
        }

        function closeVideoModal() {
            videoFrame.src = ""; // Stop video playback
            videoModal.style.display = "none";
            document.body.style.overflow = "";
        }

        if (closeVideoBtn) {
            closeVideoBtn.onclick = closeVideoModal;
        }

        if (videoModal) {
            videoModal.onclick = (e) => {
                if (e.target === videoModal) closeVideoModal();
            };
        }

        // YouTube Main Video Guide Button (Opens in-page player)
        const youtubeMainBtn = document.getElementById("youtubeMainBtn");
        if (youtubeMainBtn) {
            const ytQuery = data.youtube_query || `${data.problem_title} DIY repair tutorial`;
            youtubeMainBtn.onclick = (e) => {
                e.preventDefault();
                openVideoModal(`DIY Guide: ${data.problem_title}`, data.youtube_video_id, ytQuery);
            };
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
                            <button type="button" class="step-video-link" style="border: none; cursor: pointer;">
                                <span>▶️ Watch Step Demo Video</span>
                            </button>
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

                // Wire step video button
                const stepBtn = stepEl.querySelector(".step-video-link");
                if (stepBtn) {
                    stepBtn.addEventListener("click", (e) => {
                        e.stopPropagation();
                        openVideoModal(`Step ${step.step_num}: ${step.title}`, null, step.youtube_query);
                    });
                }

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

        // Official Vector SVG Brand Logos
        const SVG_AMAZON = `<svg class="store-svg-logo" viewBox="0 0 24 24" fill="currentColor"><path d="M14.07 14.86c-2.4 1.76-5.83 2.72-8.83 2.72-4.16 0-7.91-1.57-10.74-4.18-.21-.19-.23-.55-.02-.76.43-.44 1.01-.26 1.3.06 2.53 2.27 5.76 3.65 9.46 3.65 2.65 0 5.6-.82 7.74-2.28.32-.22.75-.12.98.2.23.32.14.77-.18.99l.29-.4zm1.18-1.28c-.28-.36-1.85-.15-2.55-.06-.21.03-.25-.15-.06-.28 1.25-.85 3.3-.6 3.62-.2.32.4-.08 2.47-1.27 3.41-.18.15-.35.07-.27-.12.27-.66.81-2.39.53-2.75zM12.5 3.5c-3.5 0-6.1 2.4-6.1 5.9 0 3.3 2.3 5.4 5.2 5.4 1.6 0 2.9-.7 3.7-1.8v1.5h2.1V3.9h-2.1v1.3c-.8-1-2.1-1.7-3.8-1.7zm.6 2c2.1 0 3.6 1.7 3.6 3.8s-1.5 3.8-3.6 3.8-3.6-1.7-3.6-3.8 1.5-3.8 3.6-3.8z"/></svg>`;
        const SVG_HOMEDEPOT = `<svg class="store-svg-logo" viewBox="0 0 24 24"><rect width="24" height="24" rx="3" fill="#F96302"/><path d="M4 6h3.2v12H4V6zm4.8 0H12v4.8h2.4V6h3.2v12h-3.2v-4.8H12V18H8.8V6zm10.4 0h2.4c1.8 0 3.2 1.4 3.2 3.2v5.6c0 1.8-1.4 3.2-3.2 3.2h-2.4V6z" fill="#FFFFFF"/></svg>`;
        const SVG_LOWES = `<svg class="store-svg-logo" viewBox="0 0 24 24"><path d="M12 2L2 9.5V21a1 1 0 001 1h18a1 1 0 001-1V9.5L12 2z" fill="#004990"/><path d="M5 11h2v7H9v2H5v-9zm4.5 0h4c1 0 1.8.8 1.8 1.8v5.4c0 1-.8 1.8-1.8 1.8h-4V11zm2 1.6v5.8h2c.2 0 .3-.1.3-.3v-5.2c0-.2-.1-.3-.3-.3h-2zm6.5-1.6h2v9h-2v-9z" fill="#FFFFFF"/></svg>`;

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
                        <a href="${amzUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-amazon">${SVG_AMAZON} Buy on Amazon</a>
                        <a href="${hdUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-homedepot">${SVG_HOMEDEPOT} Pick up at Home Depot Today</a>
                        <a href="${lowesUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-lowes">${SVG_LOWES} Lowe's Store / Ship</a>
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
                        <a href="${amzUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-amazon">${SVG_AMAZON} Buy on Amazon</a>
                        <a href="${hdUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-homedepot">${SVG_HOMEDEPOT} Home Depot</a>
                        <a href="${lowesUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-lowes">${SVG_LOWES} Lowe's</a>
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
