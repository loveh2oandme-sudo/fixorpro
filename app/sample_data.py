"""
Pre-configured realistic sample scenarios for FixOrPro.
Enables instant demonstration with in-page embedded YouTube video tutorials and rich DIY manuals.
"""

SAMPLE_SCENARIOS = {
    "running_toilet": {
        "id": "running_toilet",
        "title": "Running Toilet (Constant Water Hissing)",
        "category": "Plumbing",
        "thumbnail": "🚽",
        "image_url": "https://images.unsplash.com/photo-1584622650111-993a426fbf0a?auto=format&fit=crop&w=600&q=80",
        "description": "Water continuously trickles into the toilet bowl and the tank refills every few minutes.",
        "result": {
            "problem_title": "Worn Toilet Tank Flapper & Chain Misalignment",
            "category": "Plumbing",
            "confidence_score": "High (95%)",
            "verdict": "DIY_RECOMMENDED",
            "difficulty": "Beginner (No Special Tools)",
            "estimated_time": "15 - 20 minutes",
            "youtube_query": "how to fix running toilet replace flapper",
            "youtube_video_id": "SGdDLHbP-l0",
            "cost_comparison": {
                "diy_cost": "$8 - $16",
                "pro_cost": "$150 - $220",
                "estimated_savings": "$175",
                "savings_percentage": "92%"
            },
            "summary": "The flexible rubber flapper at the bottom of the toilet tank has hardened, mineralized, or warped over time, allowing water to continuously bleed into the bowl. Replacing the flapper and calibrating the chain length is the single easiest DIY plumbing fix and requires no pipe cutting or main water shutoff.",
            "safety_warnings": [
                "Turn off the oval emergency shut-off valve behind the toilet before detaching any internal tank parts.",
                "Place an old towel or sponge beneath the tank to catch small residual drips.",
                "Never use heavy metal wrenches on porcelain or plastic tank nuts to avoid hairline fractures."
            ],
            "tools_needed": [
                {"name": "10-inch Adjustable Slip-Joint Pliers", "amazon_search": "adjustable pliers plumbing", "homedepot_search": "pliers"}
            ],
            "materials_needed": [
                {"name": "Universal 2-inch (or 3-inch) Toilet Flapper", "est_price": "$7.99", "amazon_search": "universal toilet flapper 2 inch", "homedepot_search": "toilet flapper"},
                {"name": "Stainless Steel Flapper Chain Replacement", "est_price": "$3.99", "amazon_search": "toilet flapper chain stainless steel", "homedepot_search": "toilet chain"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "Shut off water supply and drain the tank",
                    "instruction": "Locate the oval shut-off valve on the wall directly behind the lower left side of the toilet. Turn the handle clockwise (to the right) until it stops securely. Flush the toilet once and keep holding the flush lever down until approximately 90% of the water drains into the bowl.",
                    "pro_tip": "If the shut-off valve is stiff, wrap a cloth around it for extra grip. Do NOT force it violently with large metal tools.",
                    "caution": "If the wall valve continues to drip after closing, your home's angle stop may need tightening.",
                    "youtube_query": "how to shut off toilet water supply valve"
                },
                {
                    "step_num": 2,
                    "title": "Unhook the old flapper and chain",
                    "instruction": "Lift off the ceramic tank lid and place it safely on a rug or towel. Unclip the top of the chain from the flush lever arm. Then, slide the two flexible rubber ears of the old flapper off the side mounting pegs of the vertical overflow tube and discard the worn flapper.",
                    "pro_tip": "Rub your finger along the rim of the flush drain hole to remove any mineral scale or slime before seating the new flapper.",
                    "caution": "Ceramic tank lids crack easily if set down roughly on hard tile floors.",
                    "youtube_query": "how to remove old toilet flapper"
                },
                {
                    "step_num": 3,
                    "title": "Install new flapper and calibrate chain slack",
                    "instruction": "Slide the mounting ears of your new universal flapper onto the overflow tube side pegs. Connect the chain clip to the hole on the flush arm that aligns most vertically over the flapper. Adjust the chain link position so there is roughly 1/2 inch of slight slack when the flapper rests fully closed.",
                    "pro_tip": "If the chain is too tight, the flapper will never seat and the toilet will keep running. If too loose, the flapper won't lift high enough for a full flush.",
                    "caution": "Ensure the excess chain doesn't hang down where it can get caught underneath the flapper seal.",
                    "youtube_query": "how to adjust toilet flapper chain slack"
                },
                {
                    "step_num": 4,
                    "title": "Restore water supply and perform flush test",
                    "instruction": "Turn the wall shut-off valve counterclockwise (to the left) to reopen the water line. Watch the tank fill. The fill valve should shut off automatically when the water reaches roughly 1 inch below the top of the overflow tube. Test 2-3 flushes to confirm smooth seating and zero hissing.",
                    "pro_tip": "Put 3 drops of food coloring into the tank and wait 15 minutes without flushing. If no color seeps into the bowl, your seal is 100% leak-proof!",
                    "caution": "If the hissing continues from the top of the tube, your fill valve float level may be adjusted too high.",
                    "youtube_query": "toilet food coloring leak test"
                }
            ],
            "pro_trigger_conditions": "If water is actively leaking onto your bathroom floor from the base of the toilet (wax ring failure), or if the wall shut-off valve is severely seized or corroded, stop DIY and call a licensed plumber."
        }
    },
    "disposal_jam": {
        "id": "disposal_jam",
        "title": "Garbage Disposal Humming / Jammed",
        "category": "Kitchen Appliances",
        "thumbnail": "⚙️",
        "image_url": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=600&q=80",
        "description": "Garbage disposal makes a low humming noise when turned on, but blades do not spin.",
        "result": {
            "problem_title": "Jammed Impeller Flywheel & Tripped Overload Breaker",
            "category": "Kitchen Appliances",
            "confidence_score": "High (98%)",
            "verdict": "DIY_RECOMMENDED",
            "difficulty": "Beginner (5-Minute Fix)",
            "estimated_time": "10 minutes",
            "youtube_query": "how to unjam a garbage disposal with allen wrench reset button",
            "youtube_video_id": "R6o2XlrR_fU",
            "cost_comparison": {
                "diy_cost": "$0 - $10",
                "pro_cost": "$125 - $200",
                "estimated_savings": "$160",
                "savings_percentage": "95%"
            },
            "summary": "A hard foreign object (such as a fruit pit, chicken bone, or utensil) is wedged between the rotating flywheel plate and the outer shredder ring. The humming sound proves electricity is flowing, but the internal motor safety breaker has tripped to prevent electrical burnout. This fix takes under 5 minutes.",
            "safety_warnings": [
                "NEVER insert your bare hands or fingers into the disposal opening under any circumstance.",
                "Turn off the wall switch and unplug the electrical power cord under the sink before starting.",
                "Always use long needle-nose pliers or a pick-up tool to extract dislodged debris from above."
            ],
            "tools_needed": [
                {"name": "1/4-inch Hex / Allen Key Wrench", "amazon_search": "garbage disposal hex key wrench", "homedepot_search": "garbage disposal wrench"},
                {"name": "Long Reach Needle-Nose Pliers", "amazon_search": "long reach needle nose pliers", "homedepot_search": "needle nose pliers"}
            ],
            "materials_needed": [
                {"name": "Garbage Disposal Jam-Buster Wrench", "est_price": "$6.99", "amazon_search": "disposal jam wrench", "homedepot_search": "garbage disposal wrench"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "Cut electrical power completely",
                    "instruction": "Flip the wall power switch to OFF. Look underneath the kitchen sink and physically unplug the disposal power cord from the wall electrical outlet. If the unit is hardwired, switch off the corresponding circuit breaker in your electrical panel.",
                    "pro_tip": "Double check by flipping the switch once to ensure absolutely zero humming or vibration occurs.",
                    "caution": "Never perform mechanical maintenance on an energized disposal motor.",
                    "youtube_query": "unplug garbage disposal safely"
                },
                {
                    "step_num": 2,
                    "title": "Insert hex wrench into bottom motor socket",
                    "instruction": "Look at the exact center on the underside of the disposal casing under your sink. You will find a 1/4-inch small hexagonal socket hole. Insert the 1/4-inch Allen wrench (or jam key) straight into this socket.",
                    "pro_tip": "Many disposals have a factory wrench taped to the side of the unit from original installation.",
                    "caution": "Ensure the wrench is fully seated in the socket before applying rotational force to avoid stripping the socket.",
                    "youtube_query": "where is garbage disposal allen wrench socket"
                },
                {
                    "step_num": 3,
                    "title": "Rotate back and forth to dislodge the jam",
                    "instruction": "Firmly turn the hex wrench clockwise and counterclockwise. You will initially feel strong resistance. Push firmly in both directions until the wrench begins spinning completely 360 degrees freely without catching.",
                    "pro_tip": "Work back and forth like rocking a car out of snow until the obstacle pops free.",
                    "caution": "If the hex wrench won't budge at all, use a wooden broom handle from above inserted against the blade to apply leverage.",
                    "youtube_query": "how to use hex key on garbage disposal"
                },
                {
                    "step_num": 4,
                    "title": "Extract debris and push the red reset button",
                    "instruction": "Look down into the sink drain. Use long reach needle-nose pliers to fish out the foreign object (bone, glass, coin, etc.). Then go back under the sink and firmly press the small red RESET button located near the bottom edge of the disposal casing.",
                    "pro_tip": "Run cold water for 15 seconds before flipping the power switch on to flush out any pulverized particles.",
                    "caution": "If the red button won't stay pushed in, wait 5 minutes for the motor to cool down, then push it again.",
                    "youtube_query": "where is garbage disposal red reset button"
                }
            ],
            "pro_trigger_conditions": "If water is dripping or pouring from the electrical housing or bottom seams of the disposal body, the internal seals are rusted through and the entire unit must be replaced."
        }
    },
    "drywall_hole": {
        "id": "drywall_hole",
        "title": "Punctured Drywall Hole (Door Handle Impact)",
        "category": "Walls & Drywall",
        "thumbnail": "🧱",
        "image_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=600&q=80",
        "description": "2 to 4-inch hole in drywall caused by an opening door handle smashing the sheetrock.",
        "result": {
            "problem_title": "Punctured Drywall Hole (Medium 2–4 Inch Damage)",
            "category": "Walls & Drywall",
            "confidence_score": "High (94%)",
            "verdict": "DIY_RECOMMENDED",
            "difficulty": "Intermediate (No Cutting Required)",
            "estimated_time": "35 minutes (+ drying time)",
            "youtube_query": "how to patch a drywall hole with mesh screen patch",
            "youtube_video_id": "PLGmTzEGSIY",
            "cost_comparison": {
                "diy_cost": "$15 - $28",
                "pro_cost": "$175 - $300",
                "estimated_savings": "$220",
                "savings_percentage": "88%"
            },
            "summary": "Impact damage from a door handle has penetrated through the front paper and gypsum core of the sheetrock. An aluminum mesh self-adhesive patch kit makes this repair virtually invisible once spackled and painted, without needing to cut out full square drywall sections.",
            "safety_warnings": [
                "Wear safety glasses and a simple dust mask when sanding spackle compound.",
                "Verify there are no hidden electrical wires directly behind the drywall opening before pressing hard."
            ],
            "tools_needed": [
                {"name": "Putty Knife (6-inch Flexible Stainless Blade)", "amazon_search": "putty knife 6 inch", "homedepot_search": "putty knife"},
                {"name": "Fine Grit Sanding Sponge (120-220 grit)", "amazon_search": "drywall sanding sponge fine", "homedepot_search": "sanding sponge"}
            ],
            "materials_needed": [
                {"name": "Self-Adhesive Aluminum Drywall Patch (4x4 or 6x6 inch)", "est_price": "$6.50", "amazon_search": "drywall repair patch 4x4", "homedepot_search": "drywall patch"},
                {"name": "Color-Changing Spackling Paste (Pint)", "est_price": "$8.99", "amazon_search": "drywall spackle color changing", "homedepot_search": "spackle"},
                {"name": "Spring Baseboard Door Stopper (Prevent Recurrence)", "est_price": "$3.99", "amazon_search": "spring baseboard door stop", "homedepot_search": "door stop"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "Clean and deburr the hole perimeter",
                    "instruction": "Use a utility knife or the edge of your putty knife to scrape away loose paper fibers, crumbling gypsum chunks, and frayed edges around the hole until the perimeter is flush and clean.",
                    "pro_tip": "Push slightly inward with the handle of your putty knife to bevel the outer edges inwards; this prevents the patch from bulging outwards.",
                    "caution": "Do not tear loose wall paper aggressively; cut cleanly with a blade to avoid peeling healthy paint.",
                    "youtube_query": "how to prep drywall hole before patch"
                },
                {
                    "step_num": 2,
                    "title": "Apply self-adhesive aluminum mesh patch",
                    "instruction": "Peel the backing paper off your 4x4 aluminum mesh patch. Center the solid aluminum metal plate directly over the hole and press the adhesive fiberglass perimeter firmly against the surrounding wall.",
                    "pro_tip": "Make sure the patch extends at least 1 inch beyond all edges of the damaged hole.",
                    "caution": "Do not bend or crease the aluminum plate during application.",
                    "youtube_query": "how to apply aluminum mesh drywall patch"
                },
                {
                    "step_num": 3,
                    "title": "Apply first coat of spackle (Feathering technique)",
                    "instruction": "Scoop a golf-ball sized portion of spackle onto your 6-inch putty knife. Press the paste firmly through the mesh holes to fill the cavity, then smooth outward, tapering (feathering) the edges 2-3 inches past the patch border.",
                    "pro_tip": "Use color-changing spackle (goes on pink, dries white) so you know the exact moment it is dry enough to sand.",
                    "caution": "Applying one overly thick coat will cause cracks and shrinkage; two thin coats give a professional glass-smooth finish.",
                    "youtube_query": "how to feather spackle drywall patch"
                },
                {
                    "step_num": 4,
                    "title": "Sand smooth, apply thin second coat, and touch-up paint",
                    "instruction": "Once completely white and dry (1-2 hours), gently sand the area in circular motions with a 150-grit sanding sponge until flush with the wall. Apply a paper-thin second glaze if needed, sand again, and roll matching wall paint over the patch.",
                    "pro_tip": "Install a $4 spring door stopper on the baseboard to prevent the handle from ever hitting the wall again!",
                    "caution": "Do not oversand the center or you will expose the metallic mesh texture.",
                    "youtube_query": "how to sand and paint drywall patch"
                }
            ],
            "pro_trigger_conditions": "If the hole exceeds 8 inches in diameter, or is caused by active plumbing water leaks behind the wall with dark mold present, call a professional drywall/remediation contractor."
        }
    },
    "leaking_p_trap": {
        "id": "leaking_p_trap",
        "title": "Leaking Sink P-Trap / Slip Joint",
        "category": "Plumbing",
        "thumbnail": "🚰",
        "image_url": "https://images.unsplash.com/photo-1584622781564-1d987f7333c1?auto=format&fit=crop&w=600&q=80",
        "description": "Water drips from the curved P-trap nut underneath the bathroom or kitchen vanity sink.",
        "result": {
            "problem_title": "Deteriorated Slip-Joint Rubber/Poly Washer & Loose Nut",
            "category": "Plumbing",
            "confidence_score": "High (92%)",
            "verdict": "DIY_RECOMMENDED",
            "difficulty": "Beginner (Hand Tightened)",
            "estimated_time": "20 minutes",
            "youtube_query": "how to fix leaking sink p trap slip joint washer replacement",
            "youtube_video_id": "rq1pcsULhk4",
            "cost_comparison": {
                "diy_cost": "$5 - $15",
                "pro_cost": "$160 - $240",
                "estimated_savings": "$195",
                "savings_percentage": "94%"
            },
            "summary": "The beveled poly-cone slip-joint washer inside the curved P-trap connection has dried out, cracked, or misaligned due to vibration. Replacing the 50-cent washer creates a watertight seal without needing glue or soldering.",
            "safety_warnings": [
                "Place a small basin directly under the P-trap before unscrewing nuts; standing water will drain out.",
                "Wear rubber gloves as sink trap water contains grease and soap residue."
            ],
            "tools_needed": [
                {"name": "10-inch Tongue-and-Groove Channel Lock Pliers", "amazon_search": "channel lock pliers 10 inch", "homedepot_search": "tongue and groove pliers"}
            ],
            "materials_needed": [
                {"name": "1-1/2 inch (or 1-1/4 inch) Slip-Joint Washer Kit", "est_price": "$3.49", "amazon_search": "p-trap washer kit", "homedepot_search": "slip joint washer"},
                {"name": "Plumber's Pipe Thread Seal Tape (PTFE)", "est_price": "$2.99", "amazon_search": "teflon tape plumbing", "homedepot_search": "thread seal tape"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "Position bucket and loosen slip nuts",
                    "instruction": "Place a catch bucket directly beneath the U-shaped curved pipe under the sink. Unscrew the two large plastic or metal slip nuts connecting the P-trap by turning them counterclockwise (by hand or with tongue-and-groove pliers).",
                    "pro_tip": "Modern plastic slip nuts should ideally be loosened and tightened by hand without tools to prevent stripping.",
                    "caution": "Keep your face away from directly underneath the pipe as approximately 1-2 cups of stagnant water will drop out immediately.",
                    "youtube_query": "how to remove sink p trap under sink"
                },
                {
                    "step_num": 2,
                    "title": "Inspect and clean pipe threads & mate surfaces",
                    "instruction": "Pull the curved trap assembly off. Inspect the old rubber/poly washer—it is likely cracked, flattened, or missing. Use an old rag to wipe away all hair, sludge, and soap scum from both male and female pipe ends.",
                    "pro_tip": "If the existing pipes are brittle or heavily corroded metal, replace the whole kit with an inexpensive $8 PVC kit.",
                    "caution": "Do not use drain cleaner chemicals right before doing this repair to prevent skin burns.",
                    "youtube_query": "how to clean p trap pipe threads"
                },
                {
                    "step_num": 3,
                    "title": "Install new beveled washer in correct orientation",
                    "instruction": "Slide the new slip nut onto the upper tailpiece pipe first, followed by the beveled slip washer. IMPORTANT: The tapered, angled edge of the washer MUST point downward toward the joint opening, not upward.",
                    "pro_tip": "Installing the beveled cone washer backwards is the #1 reason replacement P-traps continue to leak.",
                    "caution": "Do NOT apply plumber's putty or silicone to slip-joint washers; the compression cone does 100% of the sealing.",
                    "youtube_query": "which direction does p trap washer go"
                },
                {
                    "step_num": 4,
                    "title": "Reassemble and perform hot water leak test",
                    "instruction": "Align the P-trap straight into the wall drain outlet and sink tailpiece. Hand-tighten both slip nuts until snug, plus an extra 1/4 turn with pliers. Turn on both hot and cold sink faucets full blast for 60 seconds while wiping with a dry tissue to verify zero moisture.",
                    "pro_tip": "A completely dry paper towel rubbed on the bottom of the nuts will instantly show even a microscopic single drop of water.",
                    "caution": "Do not overtighten plastic slip nuts or the washer will deform and pinch.",
                    "youtube_query": "how to test p trap for leaks"
                }
            ],
            "pro_trigger_conditions": "If the leak is originating from inside the wall cavity behind the drywall, or if cast-iron wall drain pipes have rusted through, call a licensed plumber."
        }
    },
    "water_heater_tank": {
        "id": "water_heater_tank",
        "title": "Water Heater Tank Base Corrosion & Rust",
        "category": "Plumbing & Heating",
        "thumbnail": "🔥",
        "image_url": "https://images.unsplash.com/photo-1542013936693-884638332954?auto=format&fit=crop&w=600&q=80",
        "description": "Heavy rust, corrosion, and bubbling water stains around the bottom base seams of a residential water heater tank.",
        "result": {
            "problem_title": "Internal Tank Lining Failure & Rupture Hazard",
            "category": "Plumbing & Heating",
            "confidence_score": "High (99%)",
            "verdict": "CALL_A_PRO",
            "difficulty": "Licensed Pro Required (Hazard)",
            "estimated_time": "Pro Installation: 2 - 4 hours",
            "youtube_query": "signs water heater is about to burst fail replace",
            "youtube_video_id": "GGQatX0IUbQ",
            "cost_comparison": {
                "diy_cost": "N/A (Dangerous)",
                "pro_cost": "$1,200 - $2,200",
                "estimated_savings": "$0 (Safety Critical)",
                "savings_percentage": "0%"
            },
            "summary": "The glass-lining inside your steel water heater tank has cracked, allowing pressurized hot water to corrode through the outer steel jacket. Tank corrosion cannot be patched and represents an imminent rupture risk that could flood 40–50 gallons of water into your home. A professional tank replacement is required immediately.",
            "safety_warnings": [
                "HIGH FLOOD RISK: Do not attempt to weld, epoxy, or patch a corroded pressurized water heater tank.",
                "Shut off the gas supply line (or 240V dual-pole circuit breaker) if you detect active leaking.",
                "Know the location of your main house water shut-off valve in case of sudden rupture."
            ],
            "tools_needed": [
                {"name": "Heavy Duty Garden Hose (for emergency tank draining)", "amazon_search": "heavy duty garden hose", "homedepot_search": "garden hose"}
            ],
            "materials_needed": [
                {"name": "New 40/50-Gallon Energy-Star Water Heater (Installed by Pro)", "est_price": "$900 - $1,600", "amazon_search": "water heater 50 gallon", "homedepot_search": "water heater"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "Turn off gas or electrical power to the water heater",
                    "instruction": "If electric, switch off the double-pole 30-amp breaker in your electrical main panel. If gas, turn the dial on the bottom gas thermostat valve to OFF or PILOT, and turn the yellow gas valve handle perpendicular to the gas pipe.",
                    "pro_tip": "Never leave a leaking tank heated; heating increases internal pressure and accelerates tank rupture.",
                    "caution": "If you smell natural gas (rotten egg odor), evacuate immediately and call the gas utility.",
                    "youtube_query": "how to shut off gas to water heater emergency"
                },
                {
                    "step_num": 2,
                    "title": "Shut off cold water inlet valve on top of tank",
                    "instruction": "Look at the cold water pipe entering the top right of the water heater tank. Turn the shut-off ball valve 90 degrees (or turn the gate valve clockwise until tight) to stop pressurized water from feeding the tank.",
                    "pro_tip": "If the top valve does not stop the leak, shut off the main municipal water valve entering your house.",
                    "caution": "Pipes on top of the tank can be scalding hot; touch with care.",
                    "youtube_query": "how to turn off cold water valve to water heater"
                },
                {
                    "step_num": 3,
                    "title": "Connect garden hose to drain valve if active leaking",
                    "instruction": "Thread a standard garden hose onto the brass or plastic drain spigot at the bottom base of the tank. Run the other end of the hose to a floor drain, sump pump, or outside downhill to reduce water damage.",
                    "pro_tip": "Open a hot water faucet upstairs in the house to break vacuum suction and allow the tank to drain fast.",
                    "caution": "Water draining out can be 120°F–140°F scalding hot. Keep children and pets away.",
                    "youtube_query": "how to drain water heater with garden hose"
                },
                {
                    "step_num": 4,
                    "title": "Schedule a licensed & insured plumbing contractor",
                    "instruction": "Click below to obtain 3 competitive quotes from licensed local contractors on Thumbtack or Angi. Average replacement takes 2-4 hours and ensures full compliance with local pressure-relief valve and expansion tank building codes.",
                    "pro_tip": "Take a photo of the manufacturer label on your old unit (Model #, Serial #, Gallon capacity) to give contractors for an accurate upfront quote.",
                    "caution": "Unpermitted water heater installations can void home insurance coverage in the event of flood or fire.",
                    "youtube_query": "water heater replacement contractor quote checklist"
                }
            ],
            "pro_trigger_conditions": "Tank base corrosion, bottom seam weeping, gas burner rollout, or electrical burning odors are 100% contractor required. Do not DIY."
        }
    }
}
