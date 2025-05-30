/**
 * XWAVE Widget Extensions for ComfyUI
 * Alternative approach for color widgets
 */

import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";

console.log("[XWAVE Widgets] Loading widget extensions...");

// Add custom widget for color inputs
app.registerExtension({
    name: "XWAVE.Widgets",
    async init() {
        console.log("[XWAVE Widgets] Initializing...");
    },
    
    async setup() {
        console.log("[XWAVE Widgets] Setting up...");
    },
    
    async addCustomWidgets() {
        console.log("[XWAVE Widgets] Adding custom widgets...");
        
        // Register custom color widget type
        ComfyWidgets.COLOR = (node, inputName, inputData, app) => {
            console.log("[XWAVE Widgets] Creating COLOR widget for:", inputName);
            
            const widget = {
                type: "xwave-color",
                name: inputName,
                value: inputData[1]?.default || "#000000",
                
                draw(ctx, node, widgetWidth, y, h) {
                    const margin = 10;
                    const labelWidth = ctx.measureText(this.name).width + margin;
                    const inputWidth = widgetWidth - labelWidth - margin * 2;
                    const inputX = margin + labelWidth;
                    
                    // Draw label
                    ctx.fillStyle = "#ddd";
                    ctx.font = "14px Arial";
                    ctx.textAlign = "left";
                    ctx.textBaseline = "middle";
                    ctx.fillText(this.name, margin, y + h / 2);
                    
                    // Draw input background
                    ctx.fillStyle = "#1a1a1a";
                    ctx.fillRect(inputX, y + 2, inputWidth - 25, h - 4);
                    
                    // Draw text value
                    ctx.fillStyle = "#fff";
                    ctx.fillText(this.value || "", inputX + 5, y + h / 2);
                    
                    // Draw color preview
                    const previewSize = h - 6;
                    const previewX = widgetWidth - previewSize - margin;
                    ctx.strokeStyle = "#666";
                    ctx.lineWidth = 1;
                    ctx.strokeRect(previewX, y + 3, previewSize, previewSize);
                    
                    if (this.value && this.value.match(/^#[0-9A-Fa-f]{6}$/)) {
                        ctx.fillStyle = this.value;
                        ctx.fillRect(previewX + 1, y + 4, previewSize - 2, previewSize - 2);
                    }
                },
                
                mouse(event, pos, node) {
                    if (event.type === "pointerdown") {
                        const input = document.createElement("input");
                        input.type = "color";
                        input.value = this.value || "#000000";
                        input.style.position = "fixed";
                        input.style.opacity = "0";
                        document.body.appendChild(input);
                        
                        input.addEventListener("change", (e) => {
                            this.value = e.target.value.toUpperCase();
                            this.callback?.(this.value);
                            node.setDirtyCanvas(true, true);
                        });
                        
                        input.addEventListener("blur", () => {
                            document.body.removeChild(input);
                        });
                        
                        input.click();
                        return true;
                    }
                    return false;
                },
                
                callback: inputData[1]?.callback,
                
                serialize() {
                    return this.value;
                },
                
                configure(value) {
                    this.value = value;
                }
            };
            
            if (inputData[1]?.tooltip) {
                widget.tooltip = inputData[1].tooltip;
            }
            
            return widget;
        };
    },
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Check if this is an XWAVE node
        if (!nodeData.name.startsWith("XWave")) {
            return;
        }
        
        console.log("[XWAVE Widgets] Processing node type:", nodeData.name);
        
        // Look for color inputs and convert them
        if (nodeData.input && nodeData.input.required) {
            for (const [inputName, inputSpec] of Object.entries(nodeData.input.required)) {
                if (inputSpec[0] === "STRING" && inputSpec[1]?.display === "color") {
                    console.log("[XWAVE Widgets] Converting STRING to COLOR widget:", inputName);
                    // Change the type to our custom COLOR widget
                    inputSpec[0] = "COLOR";
                }
            }
        }
        
        if (nodeData.input && nodeData.input.optional) {
            for (const [inputName, inputSpec] of Object.entries(nodeData.input.optional)) {
                if (inputSpec[0] === "STRING" && inputSpec[1]?.display === "color") {
                    console.log("[XWAVE Widgets] Converting optional STRING to COLOR widget:", inputName);
                    // Change the type to our custom COLOR widget
                    inputSpec[0] = "COLOR";
                }
            }
        }
    }
});

console.log("[XWAVE Widgets] Widget extensions loaded!"); 