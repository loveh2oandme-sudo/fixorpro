/**
 * FixOrPro Multi-Language Translation Dictionary & Engine (i18n)
 * Fully localizes all UI, static texts, and dynamic diagnostic reports (Steps, Materials, Safety, Warnings).
 */

const TRANSLATIONS = {
    en: {
        nav_try_samples: "💡 Samples",
        nav_diagnose: "⚡ Diagnose",
        nav_find_pros: "👨‍🔧 Find Pros",
        hero_badge: "🇺🇸 Instant Home Repair Diagnostic Engine • DIY vs Pro Cost Estimator",
        hero_title: "Don’t spend $200 on a contractor for a $15 fix.",
        hero_desc: "Snap a photo of anything broken. Our AI diagnoses the problem, tells you if it's safe to DIY, and finds the exact replacement parts in 5 seconds.",
        dropzone_title: "Take or upload a photo of anything broken",
        dropzone_desc: "Toilets, garbage disposals, drywall holes, leaking pipes, water heaters, switches, doors & appliances",
        dropzone_btn_cam: "📸 Snap with Camera",
        dropzone_btn_file: "📁 Choose from Photos",
        sample_banner_title: "💡 Instant 1-Click Test Scenarios:",
        report_verdict_diy: "DIY Recommended (Beginner Friendly)",
        report_verdict_pro: "Call a Licensed Contractor (Hazard / High-Risk)",
        btn_print: "🖨️ Print / Save PDF",
        btn_share: "🔗 Share Report",
        btn_new_diag: "🔄 Diagnose Another Issue",
        sec_materials_title: "1-Click Replacement Parts & Tools",
        sec_materials_desc: "Compare prices or pick up today at your local hardware store",
        sec_materials_parts: "📦 Required Replacement Parts",
        sec_materials_tools: "🛠️ Recommended Tools",
        sec_steps_title: "Step-by-Step DIY Repair Manual",
        sec_steps_desc: "Master-contractor instructions with pro-tips, cautions & video guides",
        video_guide_title: "Watch Step-by-Step Video Tutorial",
        video_guide_desc: "Watch vetted YouTube DIY guides (This Old House, Home RenoVision, etc.)",
        video_guide_btn: "▶️ Open Video Guide",
        pro_fallback_title: "🛠️ Prefer to have an expert handle it?",
        pro_fallback_desc: "Compare free upfront quotes from licensed, insured local contractors with guaranteed workmanship.",
        pro_fallback_btn: "👨‍🔧 Get Local Pro Quotes",
        sec_safety_title: "Safety Warnings & When to Call a Pro",
        sec_safety_desc: "Essential safety checks before starting any work",
        safety_precautions_title: "⚠️ Mandatory Safety Precautions",
        safety_danger_title: "🚨 When to STOP and Call a Licensed Contractor:",
        pro_contractor_title: "Prefer to have a licensed Pro handle it?",
        pro_contractor_desc: "Find top-rated, licensed, and insured contractors in your ZIP code with upfront pricing.",
        btn_thumbtack: "🔨 Thumbtack (Compare Local Pros)",
        btn_angi: "🏠 Angi (Verified Contractors)",
        btn_yelp: "⭐ Yelp (Verified Reviews)"
    },
    ko: {
        nav_try_samples: "💡 샘플 체험",
        nav_diagnose: "⚡ 바로 진단",
        nav_find_pros: "👨‍🔧 기술자 찾기",
        hero_badge: "🤖 AI 기반 미국 주택 수리 & 비용 진단 엔진",
        hero_title: "15달러면 고칠 수리에 기술자 비용 200달러를 쓰지 마세요.",
        hero_desc: "집안의 고장 난 부위를 사진으로 찍기만 하세요. AI 시각 엔진이 5초 만에 결함을 진단하고, 직접 수리(DIY) vs 기술자 비용을 정밀 비교하며, 미국 주요 매장(아마존, 홈디포, 로우스)의 정확한 부품을 찾아드립니다.",
        dropzone_title: "집안의 고장 난 곳을 사진으로 업로드하거나 촬영하세요",
        dropzone_desc: "변기, 음식물 분쇄기, 벽 구멍, 배관 누수, 온수기, 전등 스위치, 문, 가전제품",
        dropzone_btn_cam: "📸 카메라로 직접 촬영",
        dropzone_btn_file: "📁 사진 앨범에서 선택",
        sample_banner_title: "💡 1초 만에 확인하는 5대 대표 예제:",
        report_verdict_diy: "직접 수리 권장 (DIY 추천 • 초보자 가능)",
        report_verdict_pro: "면허 기술자 필수 의뢰 (위험 / 전문 면허 필요)",
        btn_print: "🖨️ 인쇄 / PDF 견적서 저장",
        btn_share: "🔗 진단 결과 공유",
        btn_new_diag: "🔄 다른 고장 진단하기",
        sec_materials_title: "1클릭 부품 및 공구 구매 (미국 3대 스토어 실시간 가격 비교)",
        sec_materials_desc: "아마존, 홈디포, 로우스의 100% 호환 정품 부품 최저가 링크",
        sec_materials_parts: "📦 필요한 교체 부품",
        sec_materials_tools: "🛠️ 필요한 수리 공구",
        sec_steps_title: "단계별 인터랙티브 수리 가이드",
        sec_steps_desc: "전문 기술자가 감수한 안전하고 확실한 단계별 설명 및 수리 팁",
        video_guide_title: "단계별 고화질 수리 동영상 가이드",
        video_guide_desc: "미국 1위 주택 개보수 공식 채널(This Old House 등)의 검증된 튜토리얼",
        video_guide_btn: "▶️ 수리 영상 시청하기",
        pro_fallback_title: "🛠️ 직접 고치기 부담스럽거나 시간이 부족하신가요?",
        pro_fallback_desc: "면허와 보험을 갖춘 검증된 현지 기술자의 무료 사전 견적을 비교하고 시공 보증을 받으세요.",
        pro_fallback_btn: "👨‍🔧 로컬 기술자 무료 견적 받기",
        sec_safety_title: "안전 주의사항 및 기술자 호출 기준",
        sec_safety_desc: "작업을 시작하기 전 반드시 숙지해야 할 핵심 안전 확인 사항",
        safety_precautions_title: "⚠️ 필수 작업 안전 수칙",
        safety_danger_title: "🚨 작업을 즉시 중단하고 면허 기술자를 불러야 하는 상황:",
        pro_contractor_title: "우리 동네 검증된 라이선스 기술자 연결",
        pro_contractor_desc: "긴급 배관공, 전기 기술자, 핸디맨이 필요하신가요? 완벽한 보증이 포함된 무료 비교 견적을 확인하세요.",
        btn_thumbtack: "🔨 Thumbtack (현지 전문가 무료 견적)",
        btn_angi: "🏠 Angi (공식 인증 시공업체)",
        btn_yelp: "⭐ Yelp (실제 고객 평점 리뷰)"
    },
    es: {
        nav_try_samples: "💡 Ejemplos",
        nav_diagnose: "⚡ Diagnosticar",
        nav_find_pros: "👨‍🔧 Buscar Pros",
        hero_badge: "🤖 ESTIMADOR DE REPARACIONES CON IA",
        hero_title: "No gaste $200 en un contratista por un arreglo de $15.",
        hero_desc: "Tome una foto de cualquier daño en su hogar. Nuestra IA diagnostica el problema en 5 segundos, calcula los costos reales de DIY vs. Contratista y encuentra las piezas exactas.",
        dropzone_title: "Suba o tome una foto de cualquier daño en casa",
        dropzone_desc: "Inodoros, trituradores, agujeros en paneles de yeso, tuberías con fugas, calentadores de agua",
        dropzone_btn_cam: "📸 Tomar con Cámara",
        dropzone_btn_file: "📁 Elegir de Fotos",
        sample_banner_title: "💡 Escenarios de prueba instantáneos:",
        report_verdict_diy: "Recomendado Hágalo Usted Mismo (DIY)",
        report_verdict_pro: "Se Requiere Profesional con Licencia",
        btn_print: "🖨️ Imprimir / Guardar PDF",
        btn_share: "🔗 Compartir Informe",
        btn_new_diag: "🔄 Diagnosticar Otro Problema",
        sec_materials_title: "Piezas de Repuesto y Herramientas (Tiendas de EE. UU.)",
        sec_materials_desc: "Enlaces directos a repuestos en Amazon, Home Depot y Lowe's",
        sec_materials_parts: "📦 Piezas de Repuesto Requeridas",
        sec_materials_tools: "🛠️ Herramientas Recomendadas",
        sec_steps_title: "Guía de Reparación Paso a Paso",
        sec_steps_desc: "Instrucciones de contratistas profesionales con consejos, precauciones y videos",
        video_guide_title: "Ver Video Tutorial Paso a Paso",
        video_guide_desc: "Guías en video verificadas (This Old House, etc.)",
        video_guide_btn: "▶️ Abrir Guía de Video",
        pro_fallback_title: "🛠️ ¿Prefiere que un experto lo resuelva?",
        pro_fallback_desc: "Compare cotizaciones gratuitas de contratistas locales asegurados y con licencia.",
        pro_fallback_btn: "👨‍🔧 Cotizar con Profesionales",
        sec_safety_title: "Advertencias de Seguridad y Cuándo Llamar a un Pro",
        sec_safety_desc: "Verificaciones de seguridad obligatorias antes de comenzar cualquier trabajo",
        safety_precautions_title: "⚠️ Precauciones de Seguridad Obligatorias",
        safety_danger_title: "🚨 Cuándo DETENERSE y Llamar a un Contratista:",
        pro_contractor_title: "¿Prefiere que lo haga un profesional con licencia?",
        pro_contractor_desc: "Encuentre contratistas con licencia y seguro en su código postal.",
        btn_thumbtack: "🔨 Thumbtack (Cotizaciones Gratis)",
        btn_angi: "🏠 Angi (Contratistas Verificados)",
        btn_yelp: "⭐ Yelp (Reseñas Verificadas)"
    }
};

/**
 * Full Deep Localized Scenario Data for 100% Complete Translation
 */
const SCENARIO_TRANSLATIONS = {
    ko: {
        running_toilet: {
            problem_title: "마모된 변기 수조 고무 플래퍼 및 체인 장력 불량",
            difficulty: "초보자 가능 (특수 공구 불필요)",
            summary: "변기 수조 바닥의 고무 플래퍼가 노후화되어 변기통으로 물이 지속적으로 새고 있습니다. 플래퍼를 교체하고 체인 길이를 조절하는 작업은 가장 쉬운 초보자용 배관 수리이며, 주 급수 차단이나 파이프 절단이 전혀 필요하지 않습니다.",
            safety_warnings: [
                "변기 뒤편 벽에 있는 타원형 급수 밸브를 시계 방향으로 완전히 돌려 잠그고 작업하세요.",
                "수조 뚜껑(세라믹)은 타일 바닥에 세게 내려놓으면 깨지기 쉬우므로 수건 위에 안전하게 올려두세요.",
                "도기나 플라스틱 너트에 무거운 쇠렌치를 무리하게 사용하지 마세요."
            ],
            materials_needed: [
                { name: "범용 2인치 (또는 3인치) 변기 고무 플래퍼", est_price: "$7.99", amazon_search: "universal toilet flapper 2 inch", homedepot_search: "toilet flapper" },
                { name: "스테인리스 변기 플래퍼 교체용 체인", est_price: "$3.99", amazon_search: "toilet flapper chain stainless steel", homedepot_search: "toilet chain" }
            ],
            tools_needed: [
                { name: "10인치 조절식 배관 플라이어", amazon_search: "adjustable pliers plumbing", homedepot_search: "pliers" }
            ],
            steps: [
                {
                    step_num: 1,
                    title: "급수 밸브 차단 및 수조 물 빼기",
                    instruction: "변기 왼쪽 뒤편 벽에 위치한 타원형 급수 밸브를 시계 방향(오른쪽)으로 끝까지 돌려 잠급니다. 레버를 누른 상태를 유지하여 수조 내부의 물을 약 90% 이상 변기통으로 빼냅니다.",
                    pro_tip: "밸브 손잡이가 뻑뻑할 경우 마른 수건으로 감싸서 돌리면 손이 미끄러지지 않습니다.",
                    caution: "밸브를 잠근 후에도 물이 계속 뚝뚝 떨어진다면 앵글 스톱 밸브 노후를 의심해야 합니다."
                },
                {
                    step_num 2,
                    title: "기존 노후 플래퍼 및 체인 분리",
                    instruction: "세라믹 수조 뚜껑을 조심스럽게 들어 수건 위에 올려놓습니다. 플러시 레버 암에서 체인 클립을 풀고, 오버플로우 관 양쪽 돌기에 걸려 있는 노후 고무 플래퍼를 벗겨내어 버립니다.",
                    pro_tip: "새 플래퍼를 끼우기 전 배수구 림 부분을 손가락으로 닦아 물때와 이물질을 제거하면 밀폐력이 극대화됩니다.",
                    caution: "도기 뚜껑은 타일 바닥에 떨어뜨리면 쉽게 깨지므로 각별히 주의하세요."
                },
                {
                    step_num: 3,
                    title: "새 플래퍼 장착 및 체인 길이 조절",
                    instruction: "새 고무 플래퍼의 양쪽 귀를 오버플로우 관 돌기에 끼웁니다. 체인 클립을 플러시 암 구멍에 연결하고, 플래퍼가 완전히 닫혔을 때 체인이 약 1/2인치 정도 살짝 느슨하도록 링크 위치를 조절합니다.",
                    pro_tip: "체인이 너무 팽팽하면 뚜껑이 완전히 닫히지 않아 물이 계속 새고, 너무 헐렁하면 레버를 눌러도 물이 시원하게 안 내려갑니다.",
                    caution: "남는 체인이 플래퍼 밀폐 고무 아래에 끼이지 않도록 여분을 정리하세요."
                },
                {
                    step_num: 4,
                    title: "급수 밸브 개방 및 누수 최종 테스트",
                    instruction: "벽면 급수 밸브를 시계 반대 방향(왼쪽)으로 돌려 물을 채웁니다. 수조 오버플로우 관 상단에서 약 1인치 아래까지 물이 차고 자동으로 멈추는지 확인한 후, 2~3회 물을 내려 쉬익 하는 누수 소리가 사라졌는지 점검합니다.",
                    pro_tip: "수조에 식용 색소나 물감을 3방울 떨어뜨리고 15분간 물을 내리지 마세요. 변기통으로 색깔이 번지지 않으면 100% 완벽 밀폐된 것입니다!",
                    caution: "물이 오버플로우 관 꼭대기로 계속 넘쳐흐른다면 필밸브 부표(Float) 높이를 낮춰 조절해야 합니다."
                }
            ],
            pro_trigger_conditions: "변기 바닥과 욕실 타일 틈새로 물이 배어나오거나(왁스링 파손), 벽면 급수 밸브가 완전히 부식되어 헛돌 경우 즉시 면허 배관공을 부르세요."
        },
        disposal_jam: {
            problem_title: "임펠러 회전판 이물질 걸림 및 모터 과부하 차단",
            difficulty: "초보자 가능 (5분 완료)",
            summary: "단단한 이물질(과일 씨앗, 닭 뼈, 동전, 포크 등)이 회전판과 분쇄 링 사이에 끼어 모터가 멈춘 상태입니다. '웅-' 하는 모터 소리는 전기가 통하고 있음을 증명하며, 모터 소손 방지를 위해 하단 안전 브레이커가 작동한 상태입니다.",
            safety_warnings: [
                "어떠한 경우에도 맨손이나 손가락을 분쇄기 투입구 안으로 절대 넣지 마세요.",
                "작업 전 싱크대 하부 전원 코드를 콘센트에서 완전히 뽑고 벽 스위치를 끄세요.",
                "이물질을 꺼낼 때는 반드시 롱노우즈 플라이어나 집게 공구를 사용하세요."
            ],
            materials_needed: [
                { name: "음식물 분쇄기 전용 잼 해결 렌치 (Jam-Buster)", est_price: "$6.99", amazon_search: "disposal jam wrench", homedepot_search: "garbage disposal wrench" }
            ],
            tools_needed: [
                { name: "1/4인치 육각 렌치 (Allen Wrench)", amazon_search: "garbage disposal hex key wrench", homedepot_search: "garbage disposal wrench" },
                { name: "롱노우즈 플라이어 (이물질 추출용)", amazon_search: "long reach needle nose pliers", homedepot_search: "needle nose pliers" }
            ],
            steps: [
                {
                    step_num: 1,
                    title: "전원 완벽 차단",
                    instruction: "벽 스위치를 끄고, 싱크대 밑을 열어 분쇄기 전원 코드를 콘센트에서 물리적으로 뽑습니다.",
                    pro_tip: "스위치를 한번 켜서 진동이나 소리가 전혀 안 나는지 더블 체크하세요.",
                    caution: "전원이 연결된 상태에서 절대로 기계적 작업을 하지 마세요."
                },
                {
                    step_num: 2,
                    title: "분쇄기 바닥 중앙 육각 소켓에 렌치 삽입",
                    instruction: "싱크대 밑 분쇄기 본체 바닥 정중앙을 보면 1/4인치 육각 구멍(소켓)이 있습니다. 여기에 1/4인치 육각 렌치를 똑바로 꽂습니다.",
                    pro_tip: "대부분의 분쇄기는 구입 당시 본체 옆면에 전용 렌치가 테이프로 붙어 있습니다.",
                    caution: "소켓이 마모되지 않도록 렌치가 끝까지 들어갔는지 확인 후 돌리세요."
                },
                {
                    step_num: 3,
                    title: "렌치를 좌우로 왕복 회전하여 걸림 해제",
                    instruction: "렌치를 시계 방향과 반시계 방향으로 힘주어 번갈아 돌립니다. 처음에는 뻑뻑하지만 점차 360도 부드럽게 돌아갈 때까지 왕복시킵니다.",
                    pro_tip: "눈길에 빠진 자동차를 앞뒤로 흔들어 빼내듯 좌우로 흔들어주면 쉽게 풀립니다.",
                    caution: "렌치가 전혀 안 돌아갈 경우 싱크대 위에서 나무 막대(빗자루 자루)를 날에 대고 지렛대 원리로 살짝 밀어주세요."
                },
                {
                    step_num: 4,
                    title: "이물질 집게로 수거 및 빨간색 리셋 버튼 누르기",
                    instruction: "싱크대 배수구 안쪽을 들여다보고 롱노우즈 플라이어로 끼어 있던 뼈나 유리, 동전을 꺼냅니다. 그 다음 싱크대 밑 분쇄기 하단부의 작은 빨간색 RESET 버튼을 꾹 누릅니다.",
                    pro_tip: "전원을 켜기 전 찬물을 15초간 틀어 잘게 부서진 잔여물을 먼저 씻어내세요.",
                    caution: "빨간 버튼이 다시 튀어나오면 모터가 식을 때까지 5분 정도 기다린 후 다시 누르세요."
                }
            ],
            pro_trigger_conditions: "분쇄기 본체 하단 이음새나 전기 모터 하우징에서 물이 뚝뚝 새어 나온다면 내부 씰이 부식된 것이므로 본체 전체를 교체해야 합니다."
        },
        drywall_hole: {
            problem_title: "문 손잡이 충격으로 인한 석고보드(Drywall) 구멍 파손",
            difficulty: "중급 (벽 절단 불필요)",
            summary: "방문 손잡이가 벽을 강하게 때려 석고보드 중앙이 뚫린 파손입니다. 알루미늄 메쉬 자가점착 패치 키트를 사용하면 벽을 네모나게 잘라낼 필요 없이 30분 만에 감쪽같이 복구할 수 있습니다.",
            safety_warnings: [
                "퍼티(스패클) 샌딩 작업 시 보안경과 방진 마스크를 착용하세요.",
                "구멍 바로 뒤에 전선이나 배관이 지나가지 않는지 먼저 확인하세요."
            ],
            materials_needed: [
                { name: "알루미늄 메쉬 석고보드 수리 패치 (4x4인치)", est_price: "$6.50", amazon_search: "drywall repair patch 4x4", homedepot_search: "drywall patch" },
                { name: "색상 변화 스패클 퍼티 (마르면 흰색 변환)", est_price: "$8.99", amazon_search: "drywall spackle color changing", homedepot_search: "spackle" },
                { name: "스프링 도어 스토퍼 (재발 방지용)", est_price: "$3.99", amazon_search: "spring baseboard door stop", homedepot_search: "door stop" }
            ],
            tools_needed: [
                { name: "6인치 스테인리스 퍼티 나이프", amazon_search: "putty knife 6 inch", homedepot_search: "putty knife" },
                { name: "미세 샌딩 스펀지 (120-220 grit)", amazon_search: "drywall sanding sponge fine", homedepot_search: "sanding sponge" }
            ],
            steps: [
                {
                    step_num: 1,
                    title: "구멍 주변 가시 및 부스러기 정리",
                    instruction: "퍼티 나이프나 칼날로 구멍 주변의 뜯겨진 벽지 섬유와 부스러기 석고 가루를 긁어내어 표면을 평평하게 만듭니다.",
                    pro_tip: "퍼티 나이프 손잡이 끝으로 구멍 테두리를 안쪽으로 살짝 꾹꾹 눌러주면 패치가 겉으로 튀어나오지 않습니다.",
                    caution: "벽지를 무리하게 잡아당겨 뜯지 마시고 칼로 깔끔하게 잘라내세요."
                },
                {
                    step_num: 2,
                    title: "알루미늄 메쉬 패치 부착",
                    instruction: "4x4 메쉬 패치 뒷면의 보호지를 떼어내고, 금속판 중심이 구멍 중앙에 오도록 벽에 단단히 밀착시킵니다.",
                    pro_tip: "패치 크기가 손상 부위보다 사방으로 최소 1인치 이상 넓게 덮어야 튼튼합니다.",
                    caution: "부착할 때 금속판이 구겨지지 않도록 주의하세요."
                },
                {
                    step_num: 3,
                    title: "1차 퍼티 도포 (경계면 그라데이션 기법)",
                    instruction: "6인치 퍼티 나이프로 퍼티를 골프공 크기만큼 떠서 메쉬 구멍 사이로 꾹 눌러 채운 뒤, 패치 바깥쪽 2~3인치까지 얇게 펴 바릅니다.",
                    pro_tip: "바를 때는 분홍색, 마르면 흰색으로 변하는 변색 퍼티를 쓰면 샌딩 타이밍을 정확히 알 수 있습니다.",
                    caution: "한 번에 너무 두껍게 바르면 마르면서 갈라지므로 얇게 2번에 나눠 바르세요."
                },
                {
                    step_num: 4,
                    title: "샌딩, 2차 얇은 도포 및 페인트 마감",
                    instruction: "퍼티가 완전히 흰색으로 마르면 샌딩 스펀지로 원을 그리며 벽면과 완벽히 평평해질 때까지 부드럽게 갈아냅니다. 그 후 같은 색 페인트를 롤러로 칠해 마감합니다.",
                    pro_tip: "도어 스토퍼를 걸레받이에 설치하면 다시는 문 손잡이가 벽을 치지 않습니다!",
                    caution: "중앙을 너무 세게 갈면 내부 금속망이 드러나므로 주의하세요."
                }
            ],
            pro_trigger_conditions: "구멍 지름이 8인치를 초과하거나, 벽 뒤편 배관 누수로 인해 석고보드가 젖고 검은 곰팡이가 피었다면 전문 복구 업체를 불러야 합니다."
        },
        leaking_p_trap: {
            problem_title: "P-트랩 슬립 조인트 고무 와셔 경화 및 누수",
            difficulty: "초보자 가능 (손으로 조임)",
            summary: "싱크대 아래 U자형 P-트랩 배관 연결부의 원뿔형 와셔가 삭거나 어긋나서 물이 떨어지고 있습니다. 1달러짜리 새 와셔로 교체하면 접착제나 용접 없이 100% 완벽하게 방수됩니다.",
            safety_warnings: [
                "너트를 풀기 전 배관 밑에 반드시 물받이 바가지나 양동이를 받치세요. 고여 있던 물이 쏟아집니다.",
                "배관 내부 오염수에 찌꺼기가 있으므로 고무장갑을 착용하세요."
            ],
            materials_needed: [
                { name: "1-1/2인치 (또는 1-1/4인치) 슬립 조인트 고무/폴리 와셔 키트", est_price: "$3.49", amazon_search: "p-trap washer kit", homedepot_search: "slip joint washer" },
                { name: "테플론 배관 나사선 밀봉 테이프 (PTFE Tape)", est_price: "$2.99", amazon_search: "teflon tape plumbing", homedepot_search: "thread seal tape" }
            ],
            tools_needed: [
                { name: "10인치 첼라 배관 플라이어 (Channel Lock Pliers)", amazon_search: "channel lock pliers 10 inch", homedepot_search: "tongue and groove pliers" }
            ],
            steps: [
                {
                    step_num: 1,
                    title: "물받이 받치기 및 슬립 너트 풀기",
                    instruction: "싱크대 밑 U자형 배관 바로 밑에 물받이 대야를 놓습니다. 배관 양쪽 끝에 있는 큰 플라스틱/금속 슬립 너트를 시계 반대 방향으로 돌려 풉니다.",
                    pro_tip: "플라스틱 너트는 공구 없이 손으로만 돌려도 쉽게 풀립니다.",
                    caution: "너트를 풀면 배관에 고여 있던 더러운 물 1~2컵이 즉시 쏟아지므로 얼굴을 멀리하세요."
                },
                {
                    step_num: 2,
                    title: "배관 분리 및 나사산 청소",
                    instruction: "U자 배관을 분리하고 낡은 와셔를 제거합니다. 헌 헝겊으로 배관 나사산에 묻은 찌꺼기와 비누 때를 깨끗이 닦아냅니다.",
                    pro_tip: "금속 배관이 부식되어 삭았다면 8달러짜리 흰색 PVC P-트랩 세트로 통째로 교체하는 것이 가장 좋습니다.",
                    caution: "작업 직전 화학 뚫어뻥 세제를 부었다면 피부 화상 위험이 있으니 주의하세요."
                },
                {
                    step_num: 3,
                    title: "새 원뿔형 와셔를 올바른 방향으로 장착",
                    instruction: "위쪽 파이프에 슬립 너트를 먼저 끼운 뒤, 새 원뿔형 와셔를 끼웁니다. [중요]: 와셔의 뾰족하게 깎인 경사면이 반드시 결합 부위 아래쪽을 향해야 합니다.",
                    pro_tip: "원뿔 와셔를 거꾸로 끼우는 것이 수리 후에도 물이 계속 새는 가장 흔한 실수입니다.",
                    caution: "고무 슬립 조인트에는 배관용 본드나 실리콘을 바르지 마세요. 압착 패킹으로만 방수됩니다."
                },
                {
                    step_num: 4,
                    title: "배관 재조립 및 온수 누수 테스트",
                    instruction: "P-트랩을 똑바로 정렬하고 양쪽 너트를 손으로 꽉 잠근 후 플라이어로 1/4바퀴만 살짝 더 조여줍니다. 싱크대 수전을 틀어 60초간 물을 흘려보내며 마른 휴지로 닦아 물방울이 맺히는지 확인합니다.",
                    pro_tip: "마른 휴지로 너트 밑을 훑어보면 단 한 방울의 미세 누수도 즉시 확인할 수 있습니다.",
                    caution: "플라스틱 너트를 너무 무리하게 조이면 와셔가 씹혀서 오히려 물이 샙니다."
                }
            ],
            pro_trigger_conditions: "물이 벽 안쪽 석고보드 속 배관에서 새어나오거나, 벽 배수관이 주철로 되어 삭아 구멍이 났다면 면허 배관공을 부르세요."
        },
        water_heater_tank: {
            problem_title: "온수기 내부 탱크 라이닝 파손 및 하부 부식 (누수 위험)",
            difficulty: "면허 기술자 필수 (위험)",
            summary: "온수기 내부 유리 코팅이 깨져 고압 온수가 외벽 강철을 부식시키며 녹물이 배어나오는 상태입니다. 탱크 자체 부식은 땜질이나 수리가 불가능하며, 언제든 탱크가 터져 40~50갤런의 물이 집안으로 쏟아질 위험이 있어 즉시 전문 교체가 필요합니다.",
            safety_warnings: [
                "침수 위험: 부식되어 압력을 받는 온수기 탱크를 용접하거나 에폭시로 때우려 하지 마세요.",
                "가스 냄새가 나거나 누수가 보이면 즉시 가스 공급 밸브(또는 240V 전원 차단기)를 차단하세요.",
                "급작스러운 파열에 대비해 집 전체 메인 수도 밸브 위치를 확인해 두세요."
            ],
            materials_needed: [
                { name: "새 40/50갤런 에너지스타 인증 온수기 (전문가 설치용)", est_price: "$900 - $1,600", amazon_search: "water heater 50 gallon", homedepot_search: "water heater" }
            ],
            tools_needed: [
                { name: "온수기 비상 배수용 고압 정원 호스", amazon_search: "heavy duty garden hose", homedepot_search: "garden hose" }
            ],
            steps: [
                {
                    step_num: 1,
                    title: "온수기 가스 또는 전기 전원 즉시 차단",
                    instruction: "전기 온수기라면 배전반에서 30A 2극 차단기를 내립니다. 가스 온수기라면 하부 가스 밸브 다이얼을 OFF로 돌리고 노란색 가스 밸브를 파이프와 직각이 되게 돌립니다.",
                    pro_tip: "물이 새는 탱크를 계속 가열하면 내부 압력이 증가해 탱크 파열이 가속화됩니다.",
                    caution: "달걀 썩는 가스 냄새가 난다면 즉시 집 밖으로 대피하고 가스 회사에 신고하세요."
                },
                {
                    step_num: 2,
                    title: "온수기 상단 냉수 급수 밸브 잠그기",
                    instruction: "온수기 탱크 상단 오른쪽으로 들어가는 냉수 파이프의 밸브를 90도 돌려(게이트 밸브는 시계 방향으로 꽉 돌림) 탱크로 들어가는 수압을 차단합니다.",
                    pro_tip: "상단 밸브로도 물이 안 멈추면 집 메인 계량기 수도 밸브를 잠그세요.",
                    caution: "탱크 상단 파이프는 매우 뜨거울 수 있으니 화상에 주의하세요."
                },
                {
                    step_num: 3,
                    title: "하부 배수구에 호스를 연결해 물 빼기",
                    instruction: "온수기 하단 황동/플라스틱 드레인 밸브에 일반 정원 호스를 연결하고, 반대쪽을 바닥 배수구나 집 바깥으로 빼내어 물을 배출시킵니다.",
                    pro_tip: "위층 세면대의 온수 수도꼭지를 열어두면 공기가 들어가 배수가 훨씬 빠르게 진행됩니다.",
                    caution: "배출되는 물은 50도 이상의 뜨거운 물이므로 화상에 주의하세요."
                },
                {
                    step_num: 4,
                    title: "면허와 보험을 갖춘 배관 전문 기술자 예약",
                    instruction: "아래 버튼을 눌러 Thumbtack이나 Angi에서 검증된 현지 기술자 3곳의 무료 비교 견적을 받으세요. 표준 교체 작업은 2~4시간 소요되며 시 조례 규정에 맞게 완벽 시공됩니다.",
                    pro_tip: "기존 온수기 라벨(모델명, 시리얼 번호, 갤런 용량)을 미리 촬영해 두면 정확한 사전 견적을 받기 수월합니다.",
                    caution: "무면허 시공 시 향후 화재나 누수 발생 시 주택 보험 처리가 거부될 수 있습니다."
                }
            ],
            pro_trigger_conditions: "온수기 하단 녹물 배출, 이음새 누수, 가스 버너 이상 불꽃 또는 탄 냄새는 100% 면허 기술자 필수 의뢰 대상입니다."
        },
        leaking_faucet: {
            problem_title: "주방/욕실 수도꼭지 내부 카트리지 마모 및 O-링 패킹 누수",
            difficulty: "초보자 가능 (기본 수공구 사용)",
            summary: "수도꼭지를 꽉 잠가도 물이 뚝뚝 떨어지거나 손잡이 아래로 물이 배어나오는 현상은 내부 세라믹 카트리지 및 고무 O-링 패킹이 마모되었기 때문입니다. 수도꼭지 전체를 교체할 필요 없이 30분 만에 내부 카트리지만 교체하면 새것처럼 완벽히 밀폐됩니다.",
            safety_warnings: [
                "작업 시작 전 싱크대 아래에 있는 온수/냉수 급수 밸브 2개를 반드시 시계 방향으로 꽉 잠그세요.",
                "작은 육각 렌치 나사가 배수구로 빠지지 않도록 싱크대 구멍을 수건으로 먼저 막아두세요.",
                "밸브를 잠근 후 수도꼭지를 한번 틀어 파이프 안의 잔여 수압을 완전히 빼내세요."
            ],
            materials_needed: [
                { name: "호환 규격 수도꼭지 교체용 카트리지 (Cartridge)", est_price: "$14.99", amazon_search: "replacement kitchen faucet cartridge", homedepot_search: "faucet cartridge" },
                { name: "배관용 무독성 실리콘 그리스 (방수 윤활제)", est_price: "$4.50", amazon_search: "silicone faucet grease plumbers", homedepot_search: "plumbers grease" }
            ],
            tools_needed: [
                { name: "휴대용 육각 렌치 세트 (Allen Wrench Hex Key)", amazon_search: "hex key allen wrench set", homedepot_search: "allen wrench" },
                { name: "10인치 조절식 몽키 스패너 (Adjustable Wrench)", amazon_search: "adjustable wrench 10 inch", homedepot_search: "adjustable wrench" }
            ],
            steps: [
                {
                    step_num: 1,
                    title: "싱크대 아래 온수/냉수 급수 밸브 차단 및 잔류 수압 배출",
                    instruction: "싱크대 하부장을 열고 온수(왼쪽)와 냉수(오른쪽) 타원형 밸브를 시계 방향으로 끝까지 돌려 잠급니다. 수도꼭지 손잡이를 올려 물이 완전히 멈췄는지 확인합니다.",
                    pro_tip: "하부장 밸브가 너무 뻑뻑하면 수건을 감싸 쥐고 돌리세요. 그래도 안 돌아가면 집 메인 수도 밸브를 잠그세요.",
                    caution: "작은 부품이 배수구 속으로 굴러 떨어지지 않도록 배수구를 수건으로 꼭 막으세요."
                },
                {
                    step_num: 2,
                    title: "손잡이 덮개 캡 분리 및 고정 육각 나사 풀기",
                    instruction: "손잡이에 붙은 빨간/파란 온냉수 표시 플라스틱 캡을 칼날이나 일자 드라이버로 살짝 떼어냅니다. 안쪽에 보이는 작은 육각 구멍에 육각 렌치를 꽂고 반시계 방향으로 2~3바퀴 풀어 손잡이를 위로 쏙 뽑아냅니다.",
                    pro_tip: "나사를 완전히 다 뺄 필요 없이 2~3바퀴만 풀어도 손잡이가 쉽게 쑥 빠집니다.",
                    caution: "손잡이를 지렛대처럼 억지로 비틀지 마세요. 내부 황동 밸브 축이 휠 수 있습니다."
                },
                {
                    step_num: 3,
                    title: "고정 보닛 너트 분리 및 기존 마모 카트리지 인출",
                    instruction: "손으로 둥근 돔 캡을 돌려 빼낸 뒤, 몽키 스패너로 황동 고정 너트(Bonnet Nut)를 반시계 방향으로 풉니다. 너트를 제거한 후 플라이어로 카트리지 상단을 잡고 위로 똑바로 들어 올려 꺼냅니다.",
                    pro_tip: "기존 카트리지의 홈 위치(앞뒤 방향)를 스마트폰으로 사진 찍어두면 새 카트리지를 똑같은 방향으로 꽂기 쉽습니다.",
                    caution: "새 카트리지를 넣기 전 하우징 안쪽의 찌꺼기와 석회 침전물을 마른 천으로 깨끗이 닦아내세요."
                },
                {
                    step_num: 4,
                    title: "새 카트리지 장착, 너트 조임 및 누수 테스트",
                    instruction: "새 카트리지의 고무 O-링에 배관용 실리콘 그리스를 살짝 바르고, 홈에 맞춰 꾹 눌러 끼웁니다. 고정 너트를 스패너로 알맞게 조이고 손잡이를 다시 조립한 뒤, 싱크대 밑 밸브를 천천히 열어 물이 새지 않는지 테스트합니다.",
                    pro_tip: "싱크대 밑 밸브를 열 때는 수압 충격(Water Hammer)을 방지하기 위해 천천히 부드럽게 여세요.",
                    caution: "황동 고정 너트를 너무 과도하게 세게 조이면 플라스틱 카트리지가 깨질 수 있으니 적당히 조이세요."
                }
            ],
            pro_trigger_conditions: "싱크대 아래 벽 배관 연결 부위가 녹슬어 삭았거나, 수도꼭지 본체가 카운터탑에 완전히 고착되어 흔들리지 않는다면 면허 배관공을 부르세요."
        }
    }
};

/**
 * Multi-Source Smart Language Detection
 * Checks URL parameters, navigator.languages, navigator.language, system locales & user-agents.
 */
function detectBrowserLanguage() {
    // 1. URL search parameter override (e.g., ?lang=ko)
    try {
        const urlParams = new URLSearchParams(window.location.search);
        const urlLang = urlParams.get("lang");
        if (urlLang && TRANSLATIONS[urlLang]) {
            localStorage.setItem("fixorpro_user_explicit_lang", urlLang);
            return urlLang;
        }
    } catch(e) {}

    // 2. Explicit manual user choice from footer button
    const explicitChoice = localStorage.getItem("fixorpro_user_explicit_lang");
    if (explicitChoice && TRANSLATIONS[explicitChoice]) {
        return explicitChoice;
    }

    // 3. Purge legacy auto-saved 'en' pollution from previous versions
    if (localStorage.getItem("fixorpro_lang") === "en" && !explicitChoice) {
        localStorage.removeItem("fixorpro_lang");
    }

    // 4. Aggregate all browser and device language signals
    const candidates = [];
    if (navigator.languages && Array.isArray(navigator.languages)) {
        candidates.push(...navigator.languages);
    }
    if (navigator.language) candidates.push(navigator.language);
    if (navigator.userLanguage) candidates.push(navigator.userLanguage);
    if (navigator.browserLanguage) candidates.push(navigator.browserLanguage);
    if (navigator.systemLanguage) candidates.push(navigator.systemLanguage);
    if (navigator.userAgent) candidates.push(navigator.userAgent);

    try {
        const intlLocale = Intl.DateTimeFormat().resolvedOptions().locale || "";
        if (intlLocale) candidates.push(intlLocale);
        const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone || "";
        if (timeZone) candidates.push(timeZone);
    } catch (e) {}

    const lowerCandidates = candidates.map(c => (c || "").toLowerCase());

    // Priority 1: Korean match in ANY candidate language / userAgent / KakaoTalk
    for (const c of lowerCandidates) {
        if (c.startsWith("ko") || c.includes("kr") || c.includes("korean") || c.includes("kakaotalk") || c.includes("naver") || c.includes("seoul")) {
            return "ko";
        }
    }

    // Priority 2: Spanish match
    for (const c of lowerCandidates) {
        if (c.startsWith("es") || c.includes("spanish")) {
            return "es";
        }
    }

    // Default to Korean so Korean founder & Korean visitors always get Korean automatically
    return "ko";
}

let currentLanguage = detectBrowserLanguage();

function setLanguage(lang, isManual = true) {
    if (!TRANSLATIONS[lang]) lang = "en";
    currentLanguage = lang;
    if (isManual) {
        localStorage.setItem("fixorpro_user_explicit_lang", lang);
    }
    applyTranslations(lang);
    updateLangUI(lang);
}

function applyTranslations(lang) {
    const dict = TRANSLATIONS[lang] || TRANSLATIONS.en;
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (dict[key]) {
            el.textContent = dict[key];
        }
    });

    if (lang === "ko") {
        document.title = "FixOrPro | AI 기반 미국 집수리 진단 & 부품 가격 비교";
    } else if (lang === "es") {
        document.title = "FixOrPro | Diagnóstico de Reparaciones del Hogar con IA";
    } else {
        document.title = "FixOrPro | AI Home Repair Diagnostic & Cost Estimator";
    }

    document.documentElement.lang = lang;
}

function updateLangUI(lang) {
    const langNames = {
        en: "English",
        ko: "한국어",
        es: "Español"
    };
    const cycleText = document.getElementById("langCycleText");
    if (cycleText) {
        cycleText.textContent = langNames[lang] || "Language";
    }

    document.querySelectorAll(".btn-lang-toggle").forEach(btn => {
        if (btn.getAttribute("data-lang") === lang) {
            btn.classList.add("active");
            btn.style.background = "linear-gradient(135deg, #0ea5e9, #2563eb)";
            btn.style.color = "#ffffff";
            btn.style.fontWeight = "800";
        } else {
            btn.classList.remove("active");
            btn.style.background = "rgba(255,255,255,0.06)";
            btn.style.color = "var(--text-muted)";
            btn.style.fontWeight = "400";
        }
    });
}

function getLocalizedScenarioData(scenarioId, originalData) {
    const lang = currentLanguage;
    if (SCENARIO_TRANSLATIONS[lang] && SCENARIO_TRANSLATIONS[lang][scenarioId]) {
        const loc = SCENARIO_TRANSLATIONS[lang][scenarioId];
        return {
            ...originalData,
            problem_title: loc.problem_title || originalData.problem_title,
            difficulty: loc.difficulty || originalData.difficulty,
            summary: loc.summary || originalData.summary,
            safety_warnings: loc.safety_warnings || originalData.safety_warnings,
            materials_needed: loc.materials_needed || originalData.materials_needed,
            tools_needed: loc.tools_needed || originalData.tools_needed,
            steps: loc.steps || originalData.steps,
            pro_trigger_conditions: loc.pro_trigger_conditions || originalData.pro_trigger_conditions
        };
    }
    return originalData;
}

// Auto-run on load and DOM readiness
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
        applyTranslations(currentLanguage);
        updateLangUI(currentLanguage);
    });
} else {
    applyTranslations(currentLanguage);
    updateLangUI(currentLanguage);
}

// Export
window.i18n = {
    t: (key) => (TRANSLATIONS[currentLanguage] && TRANSLATIONS[currentLanguage][key]) || TRANSLATIONS.en[key] || key,
    setLanguage,
    getLanguage: () => currentLanguage,
    getLocalizedScenarioData,
    detectBrowserLanguage,
    updateLangUI,
    applyTranslations
};
