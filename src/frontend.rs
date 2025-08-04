use eframe::{egui, epi}; //bringing in the egui + app framework

struct LatencyApp { //basic struct to hold our app state
    pnl_bot_b: f64, //Bot B's profit/loss
    pnl_bot_a: Vec<(u32, f64)>, //Vec of (latency, pnl) for Bot A
    selected_latency: Option<u32>, //user's selected latency to view details
}

impl Default for LatencyApp { //default values for the app when it starts
    fn default() -> Self {
        Self {
            pnl_bot_b: 0.0, //start with no pnl
            pnl_bot_a: vec![], //empty results for Bot A
            selected_latency: None, //nothing selected initially
        }
    }
}

impl epi::App for LatencyApp { //implement the app behavior
    fn name(&self) -> &str {
        "Latency Wars Trading Bots Dashboard" //app title
    }

    fn update(&mut self, ctx: &egui::CtxRef, _frame: &mut epi::Frame) { //main update loop
        egui::CentralPanel::default().show(ctx, |ui| { //draw in the central panel
            ui.heading("Latency Wars - Trading Bots Performance"); //title

            ui.separator(); //horizontal line

            ui.label(format!("Bot B (Fast Simple Momentum) Final PnL: {:.2}", self.pnl_bot_b)); //show Bot B result

            ui.separator(); //another line

            ui.label("Bot A (Smart ML) Performance by Latency:"); //intro to list
            for (latency, pnl) in &self.pnl_bot_a { //loop through all latency entries
                if ui.selectable_label(self.selected_latency == Some(*latency), format!("Latency {} ticks: PnL {:.2}", latency, pnl)).clicked() {
                    self.selected_latency = Some(*latency); //update selection if clicked
                }
            }

            if let Some(latency) = self.selected_latency { //if something is selected
                ui.separator(); //separator
                ui.label(format!("Details for latency: {} ticks", latency)); //show which one
                ui.label("Trade stats and charts would appear here."); //placeholder for details
            }

            ui.separator(); //final line

            if ui.button("Run Evaluation").clicked() { //if user hits button
                //pretend we did some calculation and updated data
                self.pnl_bot_b = 1234.56; //hardcoded fake result
                self.pnl_bot_a = vec![ //some fake latency results
                    (1, 500.0),
                    (5, 600.0),
                    (10, 550.0),
                    (100, 1100.0),
                ];
                self.selected_latency = None; //reset selection
            }
        });
    }
}

fn main() { //entry point
    let app = LatencyApp::default(); //make our app
    let native_options = eframe::NativeOptions::default(); //just default window settings
    eframe::run_native(Box::new(app), native_options); //start the app
}
