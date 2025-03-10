use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::fs::File;
use std::io::BufWriter;

// ---------- Expander Compiler Section ----------

use expander_compiler::frontend::*;
use expander_compiler::frontend::internal::Serde;

declare_circuit!(SimpleCircuit {
    x: Variable,
    y: Variable,
});

use expander_compiler::frontend::{Define, CompileOptions, compile, M31Config};
use mersenne31::M31;

impl Define<M31Config> for SimpleCircuit<Variable> {
    fn define<Builder: RootAPI<M31Config>>(&self, api: &mut Builder) {
        api.assert_is_equal(self.x, self.y);
    }
}

/// Compile the circuit, generate a witness, and serialize the circuit & witness files.
fn compile_simple_circuit() -> Result<(), Box<dyn std::error::Error>> {
    let compile_result = compile(&SimpleCircuit::default(), CompileOptions::default())
        .map_err(|e| format!("Compile error: {:?}", e))?;
    
    let assignment = SimpleCircuit::<M31> {
        x: M31::from(123),
        y: M31::from(123),
    };
    
    let witness = compile_result
        .witness_solver
        .solve_witness(&assignment)
        .map_err(|e| format!("Witness error: {:?}", e))?;
    
    let output = compile_result.layered_circuit.run(&witness);
    if output != vec![true] {
        return Err("Circuit output invalid".into());
    }
    
    let file = File::create("circuit.txt")?;
    let writer = BufWriter::new(file);
    compile_result.layered_circuit.serialize_into(writer)?;
    
    let file = File::create("witness.txt")?;
    let writer = BufWriter::new(file);
    witness.serialize_into(writer)?;
    
    let file = File::create("witness_solver.txt")?;
    let writer = BufWriter::new(file);
    compile_result.witness_solver.serialize_into(writer)?;
    
    println!("Expander circuit compiled and files written.");
    Ok(())
}

// ---------- GKR Proof (Simulated) Section ----------

fn simulate_gkr_proof() -> Result<(), Box<dyn std::error::Error>> {
    std::thread::sleep(std::time::Duration::from_millis(100));
    println!("GKR proof simulated.");
    Ok(())
}

// ---------- PyO3 Exported Function ----------

#[pyfunction]
fn run_zkbuddy() -> PyResult<String> {
    compile_simple_circuit().map_err(|e| {
        pyo3::exceptions::PyRuntimeError::new_err(format!("Circuit compilation error: {}", e))
    })?;
    simulate_gkr_proof().map_err(|e| {
        pyo3::exceptions::PyRuntimeError::new_err(format!("GKR proof error: {}", e))
    })?;
    Ok("zkBuddy: Circuit compiled and GKR proof simulated successfully.".to_string())
}

#[pymodule]
fn zkBuddy(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(run_zkbuddy, m)?)?;
    Ok(())
}
