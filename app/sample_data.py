"""
Pre-configured realistic sample scenarios for FixOrPro.
Enables instant demonstration without needing an immediate API key.
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
            "difficulty": "Beginner",
            "estimated_time": "15 - 20 minutes",
            "cost_comparison": {
                "diy_cost": "$8 - $16",
                "pro_cost": "$150 - $220",
                "estimated_savings": "$175",
                "savings_percentage": "92%"
            },
            "summary": "The rubber flapper at the bottom of the toilet tank has degraded, allowing water to slowly leak into the bowl. This is one of the easiest DIY fixes in home repair and does not require turning off the main house water supply.",
            "safety_warnings": [
                "Turn the shut-off valve clockwise located behind the toilet before detaching parts.",
                "Have a small towel ready to soak up residual water at the bottom of the tank.",
                "Do not overtighten plastic nuts to prevent cracking the porcelain."
            ],
            "tools_needed": [
                {"name": "Adjustable Pliers", "amazon_search": "adjustable pliers plumbing", "homedepot_search": "pliers"},
                {"name": "Old Towel / Sponge", "amazon_search": "cleaning sponges", "homedepot_search": "sponge"}
            ],
            "materials_needed": [
                {"name": "Universal 2-inch or 3-inch Toilet Flapper", "est_price": "$7.99", "amazon_search": "universal toilet flapper 2 inch", "homedepot_search": "toilet flapper"},
                {"name": "Toilet Fill Valve Seal (Optional)", "est_price": "$4.50", "amazon_search": "toilet fill valve seal", "homedepot_search": "toilet fill valve"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "Shut off water & Drain tank",
                    "instruction": "Locate the oval valve behind the toilet. Turn it clockwise until tight. Flush the toilet once and hold the handle down to drain 90% of the water."
                },
                {
                    "step_num": 2,
                    "title": "Unhook the old flapper",
                    "instruction": "Remove the tank lid. Unhook the flapper chain from the flush lever arm, then unclip the two rubber ears of the flapper from the overflow tube."
                },
                {
                    "step_num": 3,
                    "title": "Install new flapper & adjust chain",
                    "instruction": "Snap the new flapper onto the overflow tube pegs. Hook the chain to the flush lever, leaving roughly 1/2 inch of slack so it closes completely when released."
                },
                {
                    "step_num": 4,
                    "title": "Turn water back on and test",
                    "instruction": "Turn the shut-off valve counterclockwise. Let the tank fill up and listen for the water to stop completely when full."
                }
            ],
            "pro_trigger_conditions": "If water is leaking onto the floor from the base of the toilet, or if the shut-off valve itself is stuck or dripping, stop and call a licensed plumber."
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
            "problem_title": "Jammed Flywheel / Tripped Internal Overload Switch",
            "category": "Kitchen Appliances",
            "confidence_score": "High (98%)",
            "verdict": "DIY_RECOMMENDED",
            "difficulty": "Beginner",
            "estimated_time": "10 minutes",
            "cost_comparison": {
                "diy_cost": "$0 - $10",
                "pro_cost": "$125 - $200",
                "estimated_savings": "$160",
                "savings_percentage": "95%"
            },
            "summary": "A small bone, fruit pit, or foreign object is wedged between the impeller blade and shredder ring. The motor is humming because power is reaching it, but the safety overload tripped to prevent burning out.",
            "safety_warnings": [
                "NEVER put your hand inside the disposal under any circumstances.",
                "Turn off the disposal wall switch and unplug the unit underneath the sink before working.",
                "Use tongs or pliers if you need to reach in to extract loose debris."
            ],
            "tools_needed": [
                {"name": "1/4-inch Hex / Allen Wrench (or Disposal Wrench)", "amazon_search": "garbage disposal hex key wrench", "homedepot_search": "garbage disposal wrench"},
                {"name": "Flashlight & Kitchen Tongs", "amazon_search": "kitchen tongs heavy duty", "homedepot_search": "tongs"}
            ],
            "materials_needed": [
                {"name": "Garbage Disposal Jam-Buster Wrench", "est_price": "$6.99", "amazon_search": "disposal jam wrench", "homedepot_search": "garbage disposal wrench"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "Cut power completely",
                    "instruction": "Turn off the wall switch and unplug the power cord located under the kitchen sink cabinet."
                },
                {
                    "step_num": 2,
                    "title": "Manually rotate flywheel from bottom",
                    "instruction": "Look at the very bottom center of the disposal unit under the sink. Insert a 1/4-inch hex wrench into the hex socket. Rotate back and forth until the wrench turns freely 360 degrees."
                },
                {
                    "step_num": 3,
                    "title": "Extract debris using tongs",
                    "instruction": "Shine a flashlight down from the sink opening. Use long kitchen tongs or needle-nose pliers to remove the dislodged object."
                },
                {
                    "step_num": 4,
                    "title": "Press red reset button & test",
                    "instruction": "Locate the small red 'Reset' button at the bottom/side of the disposal. Push it in. Plug the unit back in, run cold water, and flip the switch."
                }
            ],
            "pro_trigger_conditions": "If water is actively leaking from the bottom casing seams of the disposal, the internal seal has failed and the entire disposal unit must be replaced."
        }
    },
    "drywall_hole": {
        "id": "drywall_hole",
        "title": "Drywall Door Knob Punch Hole",
        "category": "Walls & Drywall",
        "thumbnail": "🧱",
        "image_url": "https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=600&q=80",
        "description": "Door swung open and left a 2-3 inch puncture hole in the drywall behind it.",
        "result": {
            "problem_title": "Punctured Drywall Hole (Medium 2-4 Inch Damage)",
            "category": "Walls & Drywall",
            "confidence_score": "High (94%)",
            "verdict": "DIY_RECOMMENDED",
            "difficulty": "Intermediate",
            "estimated_time": "35 minutes (+ drying time)",
            "cost_comparison": {
                "diy_cost": "$15 - $28",
                "pro_cost": "$175 - $300",
                "estimated_savings": "$220",
                "savings_percentage": "88%"
            },
            "summary": "Impact damage from a door handle has penetrated through the sheetrock. An aluminum mesh self-adhesive patch kit makes this repair virtually invisible once spackled and painted.",
            "safety_warnings": [
                "Wear a dust mask and safety glasses when sanding dried compound.",
                "Check that no electrical wires are directly behind the damaged opening before applying mesh."
            ],
            "tools_needed": [
                {"name": "Putty Knife (4 or 6-inch)", "amazon_search": "putty knife 6 inch", "homedepot_search": "putty knife"},
                {"name": "Fine Grit Sanding Sponge (120-220 grit)", "amazon_search": "drywall sanding sponge fine", "homedepot_search": "sanding sponge"}
            ],
            "materials_needed": [
                {"name": "Self-Adhesive Aluminum Drywall Patch (4x4 inch)", "est_price": "$6.50", "amazon_search": "drywall repair patch 4x4", "homedepot_search": "drywall patch"},
                {"name": "Color-Changing Spackling Paste (Pint)", "est_price": "$8.99", "amazon_search": "drywall spackle color changing", "homedepot_search": "spackle"},
                {"name": "Spring Door Stopper (Prevent future holes)", "est_price": "$3.99", "amazon_search": "spring baseboard door stop", "homedepot_search": "door stop"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "Clean and prep edges",
                    "instruction": "Use a utility knife or putty knife to scrape away loose drywall paper and pushed-in gypsum debris around the hole so the surface is flush."
                },
                {
                    "step_num": 2,
                    "title": "Apply aluminum mesh patch",
                    "instruction": "Peel off the backing paper of the aluminum mesh patch. Center it over the hole and press firmly against the wall."
                },
                {
                    "step_num": 3,
                    "title": "Apply 1st and 2nd coats of spackle",
                    "instruction": "Scoop spackling paste with the putty knife and spread across the patch, feathering the edges outward 2-3 inches beyond the mesh. Allow to dry, then apply a second thin feathering coat."
                },
                {
                    "step_num": 4,
                    "title": "Sand smooth and prime/paint",
                    "instruction": "Once completely dry, gently sand with a fine sanding sponge until seamlessly flush with the surrounding wall. Wipe clean and paint to match."
                }
            ],
            "pro_trigger_conditions": "If the hole is larger than 8 inches across or involves framing water damage, a full sheetrock drywall Dutchman patch is required."
        }
    },
    "sink_leak": {
        "id": "sink_leak",
        "title": "Bathroom / Kitchen Sink P-Trap Leak",
        "category": "Plumbing",
        "thumbnail": "🚰",
        "image_url": "https://images.unsplash.com/photo-1585909692484-9c8dfb776269?auto=format&fit=crop&w=600&q=80",
        "description": "Slow drip coming from the curved plastic/metal pipe joints underneath the sink whenever water runs.",
        "result": {
            "problem_title": "Loose Slip Nut / Degraded Rubber Slip Joint Washer",
            "category": "Plumbing",
            "confidence_score": "High (91%)",
            "verdict": "DIY_RECOMMENDED",
            "difficulty": "Beginner",
            "estimated_time": "20 minutes",
            "cost_comparison": {
                "diy_cost": "$5 - $15",
                "pro_cost": "$160 - $240",
                "estimated_savings": "$195",
                "savings_percentage": "93%"
            },
            "summary": "The slip-joint nut connection on the sink's P-trap has loosened from vibration, or the internal beveled washer has hardened and cracked over time.",
            "safety_warnings": [
                "Place a bucket directly under the P-trap to catch trapped sewer water and debris.",
                "Hand-tighten plastic PVC slip nuts first — do not overtighten with wrenches or you will strip plastic threads."
            ],
            "tools_needed": [
                {"name": "Channel Lock Pliers (for stubborn nuts)", "amazon_search": "channel lock pliers 10 inch", "homedepot_search": "tongue and groove pliers"},
                {"name": "Catch Basin / Small Bucket", "amazon_search": "small plastic bucket", "homedepot_search": "bucket"}
            ],
            "materials_needed": [
                {"name": "1-1/2 inch or 1-1/4 inch P-Trap Washer Kit", "est_price": "$3.49", "amazon_search": "p-trap washer kit", "homedepot_search": "slip joint washer"},
                {"name": "Plumber's Pipe Thread Tape (PTFE)", "est_price": "$2.99", "amazon_search": "teflon tape plumbing", "homedepot_search": "thread seal tape"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "Place bucket and loosen nuts",
                    "instruction": "Set a bucket underneath the U-shaped pipe. Unscrew the two slip-joint nuts by hand (counterclockwise). If too tight, use channel lock pliers gently."
                },
                {
                    "step_num": 2,
                    "title": "Inspect washers and clean pipe ends",
                    "instruction": "Slide the P-trap off. Inspect the conical rubber/plastic washers. Clean away soap scum, hair, and calcium buildup from the pipe threads."
                },
                {
                    "step_num": 3,
                    "title": "Replace washers with correct orientation",
                    "instruction": "Place the new beveled slip washer onto the pipe with the tapered/pointed end facing toward the joint socket."
                },
                {
                    "step_num": 4,
                    "title": "Reassemble and leak check",
                    "instruction": "Tighten the slip nuts firmly by hand, then give a 1/4 turn with pliers. Turn on the sink faucet at full pressure and check with a dry tissue for any moisture."
                }
            ],
            "pro_trigger_conditions": "If the pipe inside the wall is rusted through or if water is backing up from the main drain stack, call a licensed plumber to snake the line."
        }
    },
    "water_heater_corrosion": {
        "id": "water_heater_corrosion",
        "title": "Water Heater Tank Rust & Heavy Leak",
        "category": "Water Heaters / Gas",
        "thumbnail": "🔥",
        "image_url": "https://images.unsplash.com/photo-1542013936693-884638332954?auto=format&fit=crop&w=600&q=80",
        "description": "Heavy rust around the base of the tank with water pooling on the floor and pressure relief valve dripping.",
        "result": {
            "problem_title": "Internal Tank Wall Rupture / Critical Pressure Valve Failure",
            "category": "Water Heaters & Gas",
            "confidence_score": "High (96%)",
            "verdict": "CALL_A_PRO",
            "difficulty": "Licensed Pro Required",
            "estimated_time": "Professional Replacement (3 - 5 hrs)",
            "cost_comparison": {
                "diy_cost": "Not Recommended (Permit & Safety Hazard)",
                "pro_cost": "$1,400 - $2,600",
                "estimated_savings": "$0 (Safety Critical)",
                "savings_percentage": "0%"
            },
            "summary": "Water heater tanks have a glass-lined interior that degrades after 8-12 years. Once rust penetrates the outer jacket and water pools at the base, catastrophic tank rupture or major flooding is imminent. In addition, gas or 240V high-voltage connections require building permits and licensed plumbers in most US jurisdictions.",
            "safety_warnings": [
                "SHUT OFF the cold water inlet valve on top of the tank immediately to stop incoming water pressure.",
                "Turn off the gas valve or switch off the 240V double-pole circuit breaker on your electrical panel.",
                "DO NOT attempt to patch or weld a rusted pressurized water tank."
            ],
            "tools_needed": [
                {"name": "Garden Hose (to drain tank)", "amazon_search": "heavy duty garden hose", "homedepot_search": "garden hose"}
            ],
            "materials_needed": [
                {"name": "New 40/50 Gal Water Heater (Installed by Pro)", "est_price": "$800 - $1,500", "amazon_search": "water heater 50 gallon", "homedepot_search": "water heater"}
            ],
            "steps": [
                {
                    "step_num": 1,
                    "title": "Emergency shut-off (Water & Power)",
                    "instruction": "Turn the cold water valve clockwise. For electric models, flip the breaker off. For gas models, turn the gas control knob to 'OFF'."
                },
                {
                    "step_num": 2,
                    "title": "Drain remaining water to prevent flooding",
                    "instruction": "Connect a garden hose to the drain valve at the bottom of the water heater and run the hose to a floor drain or driveway."
                },
                {
                    "step_num": 3,
                    "title": "Get 2-3 quotes from local licensed plumbers",
                    "instruction": "Contact licensed water heater specialists in your area to pull proper municipal permits and install a new unit with warranty."
                }
            ],
            "pro_trigger_conditions": "This is a mandatory Call-a-Pro situation. Risk of 50-gallon flood, electrical shock, or gas leak."
        }
    }
}
