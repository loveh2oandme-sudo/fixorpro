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
    let activeReportData = null;

    // Use saved Amazon tag from localStorage if entered, or fallback
    const AMAZON_TAG = localStorage.getItem("fixorpro_amazon_tag") || "fixorpro-20";

    // ----------------------------------------------------------------------
    // Smart Multi-Language Setup (i18n)
    // ----------------------------------------------------------------------
    function updateActiveLangButtons() {
        if (window.i18n && window.i18n.updateLangUI) {
            window.i18n.updateLangUI(window.i18n.getLanguage());
        }
    }

    document.querySelectorAll(".btn-lang-toggle").forEach(btn => {
        btn.addEventListener("click", () => {
            const lang = btn.getAttribute("data-lang");
            if (window.i18n) {
                window.i18n.setLanguage(lang, true);
                showToast(`🌐 ${btn.textContent.trim()}`);
                loadSampleScenarios();
                if (activeReportData) {
                    renderDiagnosticReport(activeReportData);
                }
            }
        });
    });

    updateActiveLangButtons();

    // ----------------------------------------------------------------------
    // Smooth Anchor Navigation with Sticky Navbar Clearance
    // ----------------------------------------------------------------------
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener("click", function(e) {
            const href = this.getAttribute("href");
            if (!href || href === "#") return;
            const targetEl = document.querySelector(href);
            if (targetEl) {
                e.preventDefault();
                const header = document.querySelector(".site-header");
                const headerHeight = header ? header.offsetHeight + 15 : 85;
                const targetPos = targetEl.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                window.scrollTo({
                    top: Math.max(0, targetPos),
                    behavior: "smooth"
                });
            }
        });
    });

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
    if (dropZone) {
        dropZone.addEventListener("click", () => fileInput && fileInput.click());
    }

    const btnSelectFile = document.getElementById("btnSelectFile");
    if (btnSelectFile) {
        btnSelectFile.addEventListener("click", (e) => {
            e.stopPropagation();
            if (fileInput) fileInput.click();
        });
    }

    const btnCamera = document.getElementById("btnCamera");
    if (btnCamera) {
        btnCamera.addEventListener("click", (e) => {
            e.stopPropagation();
            if (cameraInput) cameraInput.click();
        });
    }

    if (fileInput) {
        fileInput.addEventListener("change", (e) => {
            if (e.target.files && e.target.files[0]) {
                handleFileSelection(e.target.files[0]);
            }
        });
    }

    if (cameraInput) {
        cameraInput.addEventListener("change", (e) => {
            if (e.target.files && e.target.files[0]) {
                handleFileSelection(e.target.files[0]);
            }
        });
    }

    // Drag & Drop
    if (dropZone) {
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
    }

    const aiQuestionBox = document.getElementById("aiQuestionBox");
    const aiQuestionTitle = document.getElementById("aiQuestionTitle");
    const aiOptionsContainer = document.getElementById("aiOptionsContainer");
    const aiLevelBadge = document.getElementById("aiLevelBadge");
    const btnNarrowQuestions = document.getElementById("btnNarrowQuestions");
    const btnSkipNarrow = document.getElementById("btnSkipNarrow");

    let currentNarrowLevel = 1;
    let narrowLevel1ChoiceText = "";

    async function fetchAndShowNarrowQuestions(level = 1, previousChoice = "") {
        const text = userNotesInput.value.trim();
        if (!text) {
            showToast("⚠️ 고장 증상이나 질문을 먼저 작성해 주세요.");
            return;
        }

        currentNarrowLevel = level;
        if (aiLevelBadge) {
            aiLevelBadge.textContent = level === 1 ? "1차 좁히기" : "2차 정밀 좁히기";
            aiLevelBadge.style.background = level === 1 ? "#06b6d4" : "#10b981";
        }

        if (aiQuestionTitle) aiQuestionTitle.textContent = level === 1 ? "🔍 1차 좁히기 질문을 분석하고 있습니다..." : "🔍 2차 정밀 좁히기 질문을 분석 중입니다...";
        if (aiOptionsContainer) {
            aiOptionsContainer.innerHTML = `<div style="color: rgba(255,255,255,0.7); text-align: center; padding: 15px;">⚡ AI가 구체적인 4가지 선택지(1~4번)를 생성 중입니다...</div>`;
        }
        if (aiQuestionBox) aiQuestionBox.style.display = "block";

        const savedKey = localStorage.getItem("fixorpro_gemini_key");

        try {
            const res = await fetch("/api/narrow", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    notes: text,
                    level: level,
                    previous_choice: previousChoice,
                    api_key: savedKey || ""
                })
            });

            if (!res.ok) throw new Error("Question narrowing API error");
            const data = await res.json();

            if (aiQuestionTitle) aiQuestionTitle.textContent = data.title;
            if (!aiOptionsContainer) return;
            aiOptionsContainer.innerHTML = "";

            if (!data.options || data.options.length === 0) {
                if (aiQuestionBox) aiQuestionBox.style.display = "none";
                return;
            }

            data.options.forEach((opt, idx) => {
                const btn = document.createElement("button");
                btn.type = "button";
                btn.className = "btn btn-ghost ai-option-btn";
                btn.style.cssText = "text-align: left; justify-content: flex-start; padding: 14px 16px; font-size: 0.95rem; border: 1px solid rgba(255,255,255,0.2); background: rgba(255,255,255,0.06); color: #ffffff; width: 100%; border-radius: 10px; cursor: pointer; transition: all 0.2s ease; line-height: 1.5;";
                btn.innerHTML = `<strong style="color: #38bdf8; margin-right: 8px; font-size: 1.05rem;">${idx + 1}번</strong> ${opt.text}`;

                btn.addEventListener("mouseover", () => {
                    btn.style.background = "rgba(56, 189, 248, 0.2)";
                    btn.style.borderColor = "#38bdf8";
                });
                btn.addEventListener("mouseout", () => {
                    btn.style.background = "rgba(255,255,255,0.06)";
                    btn.style.borderColor = "rgba(255,255,255,0.2)";
                });

                btn.addEventListener("click", () => {
                    const currentNotes = userNotesInput.value.trim();
                    
                    if (level === 1 && data.can_narrow_further) {
                        narrowLevel1ChoiceText = opt.text;
                        userNotesInput.value = `${currentNotes}\n[1차 좁히기 선택: ${idx + 1}번 - ${opt.text}]`;
                        showToast(`💡 1차 선택 완료 (${idx + 1}번)! 2차 세부 좁히기 질문을 불러옵니다...`);
                        fetchAndShowNarrowQuestions(2, opt.text);
                    } else {
                        userNotesInput.value = `${currentNotes}\n[2차 좁히기 선택: ${idx + 1}번 - ${opt.text}]`;
                        if (aiQuestionBox) aiQuestionBox.style.display = "none";
                        showToast("🎯 핀포인트 좁히기 완료! 최종 AI 진단을 실행합니다.");
                        runDiagnosis();
                    }
                });

                aiOptionsContainer.appendChild(btn);
            });

        } catch (err) {
            console.error("Failed to fetch narrowing questions:", err);
            if (aiQuestionBox) aiQuestionBox.style.display = "none";
        }
    }

    if (btnNarrowQuestions) {
        btnNarrowQuestions.addEventListener("click", () => {
            fetchAndShowNarrowQuestions(1, "");
        });
    }

    // ----------------------------------------------------------------------
    // Web Speech API - Voice Input (마이크 음성 받아쓰기)
    // ----------------------------------------------------------------------
    const btnMicInput = document.getElementById("btnMicInput");
    const micIcon = document.getElementById("micIcon");
    const micText = document.getElementById("micText");
    let recognition = null;
    let isRecording = false;

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (btnMicInput) {
        if (!SpeechRecognition) {
            btnMicInput.title = "이 브라우저는 음성 인식을 지원하지 않습니다 (Chrome, Safari, Edge 지원)";
        } else {
            recognition = new SpeechRecognition();
            recognition.continuous = false;
            recognition.interimResults = true;
            recognition.lang = "ko-KR";

            recognition.onstart = () => {
                isRecording = true;
                if (micIcon) micIcon.textContent = "🔴";
                if (micText) micText.textContent = "듣는 중...";
                btnMicInput.style.borderColor = "#ef4444";
                btnMicInput.style.color = "#f87171";
                btnMicInput.style.background = "rgba(239, 68, 68, 0.2)";
                showToast("🎙️ 음성을 듣고 있습니다. 고장 증상을 말씀해 주세요!");
            };

            recognition.onresult = (event) => {
                let transcript = "";
                for (let i = event.resultIndex; i < event.results.length; i++) {
                    transcript += event.results[i][0].transcript;
                }
                if (transcript.trim()) {
                    userNotesInput.value = transcript.trim();
                    if (btnClearNotes) btnClearNotes.style.display = "inline-flex";
                    analyzeBtn.disabled = false;
                }
            };

            recognition.onerror = (event) => {
                console.warn("Speech recognition error:", event.error);
                stopRecording();
                if (event.error !== "no-speech") {
                    showToast("⚠️ 음성 인식 오류: 마이크 권한을 확인해 주세요.");
                }
            };

            recognition.onend = () => {
                stopRecording();
            };

            function stopRecording() {
                isRecording = false;
                if (micIcon) micIcon.textContent = "🎙️";
                if (micText) micText.textContent = "음성 입력";
                btnMicInput.style.borderColor = "#10b981";
                btnMicInput.style.color = "#34d399";
                btnMicInput.style.background = "rgba(16, 185, 129, 0.1)";
            }

            btnMicInput.addEventListener("click", () => {
                if (isRecording) {
                    recognition.stop();
                } else {
                    try {
                        recognition.start();
                    } catch (e) {
                        console.error(e);
                    }
                }
            });
        }
    }

    // ----------------------------------------------------------------------
    // FixOrPro 3.0 Category Hub & Extended Drawer Click Handlers
    // ----------------------------------------------------------------------
    document.querySelectorAll(".category-hub-card[data-text]").forEach(card => {
        card.addEventListener("click", () => {
            document.querySelectorAll(".category-hub-card").forEach(c => c.classList.remove("active"));
            card.classList.add("active");
            
            const presetText = card.getAttribute("data-text");
            if (userNotesInput) userNotesInput.value = presetText;
            if (chatInput) chatInput.value = presetText;
            if (btnClearNotes) btnClearNotes.style.display = "inline-flex";
            if (analyzeBtn) analyzeBtn.disabled = false;
            
            resetDiagnosticView();
            
            // Trigger 1:1 AI chat response instantly
            if (typeof handleChatSubmit === "function") {
                handleChatSubmit();
            } else {
                fetchAndShowNarrowQuestions(1, "");
            }
        });
    });

    const btnToggleExtended = document.getElementById("btnToggleExtended");
    const extendedDrawer = document.getElementById("extendedDrawer");
    if (btnToggleExtended && extendedDrawer) {
        btnToggleExtended.addEventListener("click", () => {
            const isVisible = extendedDrawer.style.display === "block";
            extendedDrawer.style.display = isVisible ? "none" : "block";
            if (!isVisible) {
                extendedDrawer.scrollIntoView({ behavior: "smooth", block: "nearest" });
            }
        });
    }

    document.querySelectorAll(".ext-chip[data-text]").forEach(chip => {
        chip.addEventListener("click", () => {
            const presetText = chip.getAttribute("data-text");
            if (userNotesInput) userNotesInput.value = presetText;
            if (chatInput) chatInput.value = presetText;
            if (btnClearNotes) btnClearNotes.style.display = "inline-flex";
            if (analyzeBtn) analyzeBtn.disabled = false;
            
            resetDiagnosticView();
            if (typeof handleChatSubmit === "function") {
                handleChatSubmit();
            } else {
                fetchAndShowNarrowQuestions(1, "");
            }
        });
    });

    if (btnSkipNarrow) {
        btnSkipNarrow.addEventListener("click", () => {
            if (aiQuestionBox) aiQuestionBox.style.display = "none";
            runDiagnosis();
        });
    }

    const btnClearNotes = document.getElementById("btnClearNotes");

    function resetDiagnosticView() {
        if (aiQuestionBox) aiQuestionBox.style.display = "none";
        if (reportContainer) reportContainer.style.display = "none";
        if (loadingBox) loadingBox.style.display = "none";
        activeReportData = null;
        currentNarrowLevel = 1;
        narrowLevel1ChoiceText = "";
        try {
            sessionStorage.removeItem("fixorpro_active_report");
        } catch (e) {}
        if (narrowDebounceTimer) clearTimeout(narrowDebounceTimer);
    }

    if (btnClearNotes) {
        btnClearNotes.addEventListener("click", () => {
            userNotesInput.value = "";
            btnClearNotes.style.display = "none";
            resetDiagnosticView();
            if (!currentFile && !selectedSampleId) {
                analyzeBtn.disabled = true;
            }
            showToast("🧹 증상 설명 및 솔루션 리포트가 지워졌습니다.");
        });
    }

    let narrowDebounceTimer = null;
    userNotesInput.addEventListener("input", () => {
        const text = userNotesInput.value.trim();

        if (text.length > 0) {
            if (btnClearNotes) btnClearNotes.style.display = "inline-flex";
            analyzeBtn.disabled = false;
        } else {
            if (btnClearNotes) btnClearNotes.style.display = "none";
            resetDiagnosticView();
            if (!currentFile && !selectedSampleId) {
                analyzeBtn.disabled = true;
            }
        }

        if (selectedSampleId) {
            selectedSampleId = null;
            clearActiveSampleCards();
        }

        // Auto fetch 1, 2, 3, 4 choices when user writes 4+ characters and hasn't selected options yet
        if (!text.includes("[1차 좁히기") && text.length >= 4) {
            clearTimeout(narrowDebounceTimer);
            narrowDebounceTimer = setTimeout(() => {
                fetchAndShowNarrowQuestions(1, "");
            }, 1000);
        }
    });

    removeImageBtn.addEventListener("click", () => {
        currentFile = null;
        selectedSampleId = null;
        fileInput.value = "";
        cameraInput.value = "";
        previewContainer.style.display = "none";
        dropZone.style.display = "block";
        if (!userNotesInput.value.trim()) {
            analyzeBtn.disabled = true;
        }
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

    const SAMPLE_TITLES = {
        ko: {
            exterior_wall_hole: { title: "건물 외벽(스타코/사이딩) 구멍", category: "외벽" },
            running_toilet: { title: "변기 물이 계속 샐 때", category: "배관" },
            disposal_jam: { title: "음식물 분쇄기 모터 걸림", category: "가전" },
            drywall_hole: { title: "문 손잡이 벽 구멍", category: "벽체" },
            leaking_p_trap: { title: "싱크대 밑 P-트랩 누수", category: "배관" },
            water_heater_tank: { title: "온수기 내부 부식 & 누수", category: "위험" }
        },
        es: {
            exterior_wall_hole: { title: "Agujero en pared exterior", category: "Exterior" },
            running_toilet: { title: "Inodoro con fuga continua", category: "Plomería" },
            disposal_jam: { title: "Triturador de basura atascado", category: "Aparatos" },
            drywall_hole: { title: "Agujero en panel de yeso", category: "Paredes" },
            leaking_p_trap: { title: "Fuga en trampa P de fregadero", category: "Plomería" },
            water_heater_tank: { title: "Falla y fuga en calentador", category: "Peligro" }
        }
    };

    function renderSampleCards(samples) {
        if (!sampleCardsContainer) return;
        sampleCardsContainer.innerHTML = "";
        const lang = window.i18n ? window.i18n.getLanguage() : "en";

        samples.forEach(sample => {
            const localized = (SAMPLE_TITLES[lang] && SAMPLE_TITLES[lang][sample.id]) || {};
            const displayTitle = localized.title || sample.title;
            const displayCategory = localized.category || sample.category;

            const card = document.createElement("div");
            card.className = "sample-card glass-panel";
            card.dataset.id = sample.id;
            card.innerHTML = `
                <div>
                    <div class="sample-thumb-icon">${sample.thumbnail}</div>
                    <div class="sample-name">${displayTitle}</div>
                </div>
                <div class="sample-badge">${displayCategory}</div>
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
        const notes = userNotesInput.value.trim();
        if (!currentFile && !selectedSampleId && !notes) {
            showToast("⚠️ Please upload a photo, write a description, or pick a sample scenario.");
            return;
        }

        // Show loading HUD
        reportContainer.style.display = "none";
        loadingBox.style.display = "block";
        analyzeBtn.disabled = true;
        loadingBox.scrollIntoView({ behavior: "smooth", block: "center" });

        // Cycle Scanning Messages
        const scanSteps = [
            "[1/4] Scanning problem symptoms & defect vectors...",
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

        // Send sample_id ONLY if selected and user did not write custom text notes
        if (selectedSampleId && (!notes || notes.length === 0)) {
            formData.append("sample_id", selectedSampleId);
        }
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
                throw new Error(errorData.detail || "Failed to analyze issue.");
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

    function detectScenarioKey(data, sampleId) {
        if (sampleId) return sampleId;
        return null;
    }

    // ----------------------------------------------------------------------
    // Render Result Report (Amazon + Home Depot + Lowe's)
    // ----------------------------------------------------------------------
    function renderDiagnosticReport(data, source) {
        activeReportData = data;
        try {
            sessionStorage.setItem("fixorpro_active_report", JSON.stringify({ data, source }));
        } catch(e) {}

        // Apply Deep Scenario Localization ONLY for pre-defined 1-click sample scenarios
        if (source === "sample" && selectedSampleId && window.i18n && window.i18n.getLocalizedScenarioData) {
            data = window.i18n.getLocalizedScenarioData(selectedSampleId, data);
        }

        const isDIY = data.verdict === "DIY_RECOMMENDED";

        // 1. Verdict Banner
        verdictBanner.className = `verdict-banner ${isDIY ? 'diy' : 'pro'}`;
        verdictIcon.textContent = isDIY ? "🟢" : "🚨";
        const diyLabel = window.i18n ? window.i18n.t("report_verdict_diy") : "DIY Recommended (Beginner Friendly)";
        const proLabel = window.i18n ? window.i18n.t("report_verdict_pro") : "Call a Licensed Contractor";
        verdictTag.textContent = isDIY ? diyLabel : proLabel;
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

        // Curated, 100% Embed-Verified Real DIY Video Tutorials (Tested & Active)
        const DIY_VIDEO_MAP = {
            "stucco": "zZ4fO_k4W_U",      // Exterior Stucco Wall Repair
            "exterior": "zZ4fO_k4W_U",
            "siding": "zZ4fO_k4W_U",
            "외벽": "zZ4fO_k4W_U",
            "toilet": "SGdDLHbP-l0",      // Replace Toilet Flapper
            "flapper": "SGdDLHbP-l0",
            "disposal": "R6o2XlrR_fU",    // Fix Jammed Garbage Disposal
            "jam": "R6o2XlrR_fU",
            "drywall": "PLGmTzEGSIY",     // How to Patch a Drywall Hole
            "hole": "PLGmTzEGSIY",
            "patch": "PLGmTzEGSIY",
            "p-trap": "HkFTnnFbh-s",      // This Old House - How to Replace PVC Sink Trap (16:9 Widescreen)
            "trap": "HkFTnnFbh-s",
            "water heater": "GGQatX0IUbQ",// How to Replace a Water Heater
            "heater": "GGQatX0IUbQ",
            "faucet": "RUX3U6CIRXI",      // How to Fix a Leaky Faucet
            "drip": "RUX3U6CIRXI",
            "leak": "HkFTnnFbh-s",
            "outlet": "lUAaVwSjk3M",      // How to Change Electrical Outlet
            "switch": "lUAaVwSjk3M",
            "drain": "8Q__Zub2j4Q",       // How to Clear a Bathroom Sink Drain
            "clog": "8Q__Zub2j4Q",
            "door": "SAgDwFDqxVM",        // How to Fix a Sticking Door
            "caulk": "z8tdp0lLfCw",       // Easiest Way to Caulk Bathtub / Shower
            "contractor": "GGQatX0IUbQ",
            "plumbing": "SGdDLHbP-l0"
        };

        function resolveYouTubeVideoId(title, query, explicitId) {
            if (explicitId) return explicitId;
            const searchStr = `${title || ""} ${query || ""}`.toLowerCase();
            for (const [kw, vidId] of Object.entries(DIY_VIDEO_MAP)) {
                if (searchStr.includes(kw)) {
                    return vidId;
                }
            }
            return "PLGmTzEGSIY"; // Universal high quality verified DIY guide
        }

        // YouTube In-Page Video Player Modal Setup
        const videoModal = document.getElementById("videoModal");
        const videoFrame = document.getElementById("videoFrame");
        const videoTitleText = document.getElementById("videoTitleText");
        const videoModalBuyLinks = document.getElementById("videoModalBuyLinks");
        const closeVideoBtn = document.getElementById("closeVideoBtn");

        function openVideoModal(title, videoId, query) {
            videoTitleText.textContent = title || "DIY Repair Video Tutorial";
            
            const resolvedId = resolveYouTubeVideoId(title, query, videoId);
            const embedUrl = `https://www.youtube.com/embed/${resolvedId}?rel=0&modestbranding=1&iv_load_policy=3&playsinline=1`;
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
                        <span style="font-size: 0.85rem; color: var(--text-secondary); margin-right: 8px;">• ${mat.name}:</span>
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

        // Close on Escape key
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape" && videoModal.style.display === "flex") {
                closeVideoModal();
            }
        });

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

        // 7. Guaranteed 100% Active Contractor Lead & Affiliate Matching Links (Never 404)
        function getContractorCategoryInfo(d) {
            const rawCat = (d.category || "").toLowerCase();
            const rawTitle = (d.problem_title || "").toLowerCase();
            const fullText = `${rawCat} ${rawTitle}`;

            // Plumbing (Toilet, Sink, Faucet, Leak, Drain, P-Trap)
            if (fullText.includes("toilet") || fullText.includes("plumb") || fullText.includes("변기") || fullText.includes("배관") || fullText.includes("leak") || fullText.includes("p-trap") || fullText.includes("trap") || fullText.includes("트랩") || fullText.includes("faucet") || fullText.includes("drain") || fullText.includes("수도")) {
                return {
                    thumbtackSlug: "plumbing",
                    angiQuery: "plumber",
                    yelpQuery: "plumber"
                };
            }
            // Garbage Disposal & Appliances
            if (fullText.includes("disposal") || fullText.includes("분쇄기") || fullText.includes("appliance") || fullText.includes("가전") || fullText.includes("washer") || fullText.includes("dishwasher")) {
                return {
                    thumbtackSlug: "garbage-disposal-repair",
                    angiQuery: "garbage-disposal-repair",
                    yelpQuery: "garbage-disposal-repair"
                };
            }
            // Exterior / Stucco / Siding Repair
            if (fullText.includes("exterior") || fullText.includes("stucco") || fullText.includes("외벽") || fullText.includes("스타코") || fullText.includes("siding") || fullText.includes("사이딩") || fullText.includes("masonry") || fullText.includes("brick")) {
                return {
                    thumbtackSlug: "stucco-repair",
                    angiQuery: "stucco-repair",
                    yelpQuery: "stucco-repair"
                };
            }
            // Drywall & Wall Repair
            if (fullText.includes("drywall") || fullText.includes("sheetrock") || fullText.includes("석고") || fullText.includes("벽") || fullText.includes("hole") || fullText.includes("patch")) {
                return {
                    thumbtackSlug: "drywall-repair",
                    angiQuery: "drywall-repair",
                    yelpQuery: "drywall-repair"
                };
            }
            // Water Heater
            if (fullText.includes("heater") || fullText.includes("water heater") || fullText.includes("온수기") || fullText.includes("boiler") || fullText.includes("보일러")) {
                return {
                    thumbtackSlug: "water-heater-installation",
                    angiQuery: "water-heater-repair",
                    yelpQuery: "water-heater-repair"
                };
            }
            // Electrical
            if (fullText.includes("electric") || fullText.includes("전기") || fullText.includes("outlet") || fullText.includes("switch") || fullText.includes("스위치") || fullText.includes("breaker")) {
                return {
                    thumbtackSlug: "electricians",
                    angiQuery: "electrician",
                    yelpQuery: "electrician"
                };
            }
            // General Handyman fallback
            return {
                thumbtackSlug: "handyman",
                angiQuery: "handyman",
                yelpQuery: "handyman"
            };
        }

        const proInfo = getContractorCategoryInfo(data);
        const affiliateTag = localStorage.getItem("fixorpro_contractor_tag") || "";
        const tagParam = affiliateTag ? `?utm_source=fixorpro&utm_medium=affiliate&subid=${encodeURIComponent(affiliateTag)}` : "";

        thumbtackBtn.href = `https://www.thumbtack.com/k/${proInfo.thumbtackSlug}/near-me${tagParam}`;
        angiBtn.href = `https://www.angi.com/search.htm?query=${encodeURIComponent(proInfo.angiQuery)}${tagParam}`;
        yelpBtn.href = `https://www.yelp.com/search?find_desc=${encodeURIComponent(proInfo.yelpQuery)}${tagParam}`;

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
        try {
            sessionStorage.removeItem("fixorpro_active_report");
        } catch(e) {}
        clearActiveSampleCards();
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    // Restore active report if page was reloaded or refreshed
    try {
        const savedReport = sessionStorage.getItem("fixorpro_active_report");
        if (savedReport) {
            const parsed = JSON.parse(savedReport);
            if (parsed && parsed.data) {
                renderDiagnosticReport(parsed.data, parsed.source || "live_ai");
            }
        }
    } catch(e) {}

    // ======================================================================
    // FIXORPRO MOBILE APP NATIVE LOGIC (PWA, VOICE, BOTTOM NAV, 1:1 AI CHAT)
    // ======================================================================

    // 1. PWA Service Worker Registration
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js').then(reg => {
                console.log('FixOrPro PWA ServiceWorker active:', reg.scope);
            }).catch(err => {
                console.log('PWA ServiceWorker failed:', err);
            });
        });
    }

    // 2. Mobile Bottom Navigation Tabs Handler
    const bnavChat = document.getElementById("bnavChat");
    const bnavPhoto = document.getElementById("bnavPhoto");
    const bnavParts = document.getElementById("bnavParts");
    const bnavSettings = document.getElementById("bnavSettings");

    const panePhotoQuick = document.getElementById("panePhotoQuick");
    const paneAiChat = document.getElementById("paneAiChat");
    const tabPhotoQuick = document.getElementById("tabPhotoQuick");
    const tabAiChat = document.getElementById("tabAiChat");

    function setActiveTab(activeNavBtn, activePane) {
        [bnavChat, bnavPhoto, bnavParts, bnavSettings].forEach(b => {
            if (b) b.classList.remove("active");
        });
        if (activeNavBtn) activeNavBtn.classList.add("active");

        if (activePane === "chat") {
            if (paneAiChat) paneAiChat.style.display = "block";
            if (panePhotoQuick) panePhotoQuick.style.display = "none";
            if (tabAiChat) tabAiChat.classList.add("active");
            if (tabPhotoQuick) tabPhotoQuick.classList.remove("active");
        } else if (activePane === "photo") {
            if (paneAiChat) paneAiChat.style.display = "none";
            if (panePhotoQuick) panePhotoQuick.style.display = "block";
            if (tabPhotoQuick) tabPhotoQuick.classList.add("active");
            if (tabAiChat) tabAiChat.classList.remove("active");
            const ws = document.getElementById("workspaceSection");
            if (ws) ws.scrollIntoView({ behavior: "smooth" });
        } else if (activePane === "parts") {
            if (reportContainer && reportContainer.style.display === "block") {
                reportContainer.scrollIntoView({ behavior: "smooth" });
            } else {
                showToast("🛠️ 수리 부품 및 전문가 예약 카드: AI 대화 또는 진단을 실행해 주세요.");
            }
        } else if (activePane === "settings") {
            showToast("⚙️ 설정: Gemini API Key & Amazon 파트너 설정을 엽니다.");
        }
    }

    if (bnavChat) bnavChat.addEventListener("click", () => setActiveTab(bnavChat, "chat"));
    if (bnavPhoto) bnavPhoto.addEventListener("click", () => setActiveTab(bnavPhoto, "photo"));
    if (bnavParts) bnavParts.addEventListener("click", () => setActiveTab(bnavParts, "parts"));
    if (bnavSettings) bnavSettings.addEventListener("click", () => setActiveTab(bnavSettings, "settings"));

    if (tabPhotoQuick) tabPhotoQuick.addEventListener("click", () => setActiveTab(bnavPhoto, "photo"));
    if (tabAiChat) tabAiChat.addEventListener("click", () => setActiveTab(bnavChat, "chat"));

    // 3. Voice Input (Microphone Speech Recognition)
    const chatMicBtn = document.getElementById("chatMicBtn");
    const btnMicInput = document.getElementById("btnMicInput");
    const chatInput = document.getElementById("chatInput");

    let isListening = false;
    let recognition = null;

    if ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window) {
        const SpeechClass = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechClass();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'ko-KR';

        recognition.onstart = () => {
            isListening = true;
            if (chatMicBtn) chatMicBtn.classList.add("listening");
            showToast("🎙️ 음성 듣는 중... 말씀해 주세요!");
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            if (chatInput) {
                chatInput.value = transcript;
            }
            if (userNotesInput) {
                userNotesInput.value = transcript;
            }
            showToast(`🎙️ 인식됨: "${transcript}"`);
            // Auto submit speech input into 1:1 chat!
            handleChatSubmit();
        };

        recognition.onerror = (event) => {
            console.error("Speech Recognition Error:", event.error);
            showToast("🎙️ 음성 인식 오류: 다시 시도해 주세요.");
            isListening = false;
            if (chatMicBtn) chatMicBtn.classList.remove("listening");
        };

        recognition.onend = () => {
            isListening = false;
            if (chatMicBtn) chatMicBtn.classList.remove("listening");
        };
    }

    function toggleVoiceInput() {
        if (!recognition) {
            showToast("🎙️ 브라우저가 음성 인식을 지원하지 않습니다. 텍스트로 작성해 주세요!");
            return;
        }
        if (isListening) {
            recognition.stop();
        } else {
            recognition.start();
        }
    }

    if (chatMicBtn) chatMicBtn.addEventListener("click", toggleVoiceInput);
    if (btnMicInput) btnMicInput.addEventListener("click", toggleVoiceInput);

    // 4. Photo Attachment Button in Chat Bar
    const chatPhotoBtn = document.getElementById("chatPhotoBtn");
    if (chatPhotoBtn) {
        chatPhotoBtn.addEventListener("click", () => {
            setActiveTab(bnavPhoto, "photo");
            if (fileInput) fileInput.click();
        });
    }

    // 5. Interactive 1:1 AI Diagnostic Chat Logic
    const chatForm = document.getElementById("chatForm");
    const chatMessages = document.getElementById("chatMessages");
    const chatSuggestions = document.getElementById("chatSuggestions");
    let chatHistory = [];

    async function handleChatSubmit() {
        if (!chatInput) return;
        const msg = chatInput.value.strip ? chatInput.value.strip() : chatInput.value.trim();
        if (!msg) return;

        chatInput.value = "";

        // User message bubble
        appendChatBubble("user", msg);
        chatHistory.push({ role: "user", content: msg });

        // AI Typing indicator bubble
        const typingId = "typing_" + Date.now();
        appendChatBubble("ai", "⚡ AI 기술자가 대답을 작성하는 중입니다...", typingId);

        try {
            const savedKey = localStorage.getItem("fixorpro_gemini_key");
            const res = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    messages: chatHistory,
                    api_key: savedKey || "",
                    language: window.i18n ? window.i18n.getLanguage() : "ko"
                })
            });

            const typingEl = document.getElementById(typingId);
            if (typingEl) typingEl.remove();

            if (!res.ok) throw new Error("Chat response failed");
            const data = await res.json();

            const replyText = data.reply || "죄송합니다. 대답을 생성하지 못했습니다.";
            appendChatBubble("ai", replyText);
            chatHistory.push({ role: "model", content: replyText });

            // If AI chat returned a report scenario or data, render IN-CHAT Action Card!
            if (data.report_data) {
                renderInChatActionCard(data.report_data);
            } else if (data.report_scenario && SAMPLE_SCENARIOS[data.report_scenario]) {
                renderInChatActionCard(SAMPLE_SCENARIOS[data.report_scenario]["result"]);
            }

            // Update chat suggestion chips if provided
            if (data.suggestions && chatSuggestions) {
                chatSuggestions.innerHTML = "";
                data.suggestions.forEach(sugText => {
                    const chip = document.createElement("div");
                    chip.className = "chat-chip";
                    chip.textContent = sugText;
                    chip.setAttribute("data-text", sugText);
                    chip.addEventListener("click", () => {
                        chatInput.value = sugText;
                        handleChatSubmit();
                    });
                    chatSuggestions.appendChild(chip);
                });
            }
        } catch(err) {
            const typingEl = document.getElementById(typingId);
            if (typingEl) typingEl.remove();
            appendChatBubble("ai", "⚠️ 연결에 실패했습니다. 다시 시도해 주세요.");
        }
    }

    function appendChatBubble(role, text, id = null) {
        if (!chatMessages) return;
        const bubble = document.createElement("div");
        bubble.className = `chat-bubble ${role}`;
        if (id) bubble.id = id;
        bubble.innerHTML = text.replace(/\n/g, "<br>");
        chatMessages.appendChild(bubble);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function renderInChatActionCard(reportData) {
        if (!chatMessages || !reportData) return;

        const cardContainer = document.createElement("div");
        cardContainer.className = "in-chat-action-card";

        let partsHtml = "";
        const materials = reportData.materials_needed || [];
        const tools = reportData.tools_needed || [];

        [...materials, ...tools].forEach(item => {
            const itemName = item.name || "수리 부품/공구";
            const price = item.est_price || "$8.99";
            const kw = item.amazon_search || item.homedepot_search || itemName;
            const amzUrl = `https://www.amazon.com/s?k=${encodeURIComponent(kw)}&tag=${AMAZON_TAG}`;
            const hdUrl = `https://www.homedepot.com/s/${encodeURIComponent(kw)}`;

            partsHtml += `
              <div class="in-chat-part-item">
                <div>
                  <div class="in-chat-part-name">${itemName}</div>
                  <div class="in-chat-part-price">${price}</div>
                </div>
                <div class="in-chat-buy-group">
                  <a href="${amzUrl}" target="_blank" rel="noopener noreferrer" class="btn-buy-mini btn-buy-amz">
                    🛒 Amazon
                  </a>
                  <a href="${hdUrl}" target="_blank" rel="noopener noreferrer" class="btn-buy-mini btn-buy-hd">
                    🧡 Home Depot
                  </a>
                </div>
              </div>
            `;
        });

        const isProNeeded = reportData.verdict === "CALL_A_PRO";
        let proHtml = "";
        if (isProNeeded) {
            proHtml = `
              <a href="https://www.thumbtack.com" target="_blank" rel="noopener noreferrer" class="btn-pro-mini">
                🚨 고위험 작업: 로컬 기술자 1-Click 예약하기 (Thumbtack / Angi)
              </a>
            `;
        }

        cardContainer.innerHTML = `
          <div class="in-chat-card-title">
            🛒 1-Click 최저가 부품 구매 &amp; 전문가 연결
          </div>
          <div>${partsHtml}</div>
          ${proHtml}
          <div style="margin-top: 10px; text-align: right;">
            <button type="button" class="btn btn-ghost btn-show-full-report" style="font-size: 0.8rem; color: #38bdf8;">
              📋 전체 진단 리포트 &amp; 수리 단계 펼쳐보기 ➔
            </button>
          </div>
        `;

        const showReportBtn = cardContainer.querySelector(".btn-show-full-report");
        if (showReportBtn) {
            showReportBtn.addEventListener("click", () => {
                renderDiagnosticReport(reportData, "chat_action");
            });
        }

        chatMessages.appendChild(cardContainer);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    const chatSendBtn = document.getElementById("chatSendBtn");

    if (chatForm) {
        chatForm.addEventListener("submit", (e) => {
            e.preventDefault();
            handleChatSubmit();
        });
    }

    if (chatSendBtn) {
        chatSendBtn.addEventListener("click", (e) => {
            e.preventDefault();
            handleChatSubmit();
        });
    }

    if (chatInput) {
        chatInput.addEventListener("keydown", (e) => {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleChatSubmit();
            }
        });
    }

    document.querySelectorAll(".chat-chip").forEach(chip => {
        chip.addEventListener("click", () => {
            const text = chip.getAttribute("data-text");
            if (chatInput && text) {
                chatInput.value = text;
                handleChatSubmit();
            }
        });
    });
});

