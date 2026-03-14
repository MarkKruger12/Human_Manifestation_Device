# Human Manifestation Device (v1.0)

## 0.0 Overview: The Geometric Forge
The **Human Manifestation Device** is a 64-bit analytical framework designed to map the topological transitions of biological sequences. By utilizing **Belnap-W Tesseract Physics**, this project identifies the specific coordinates where matter manifests from a state of general conduction to a specific biological instruction.

## 1.0 The 6-Bit I-Ching Logic Gate
Traditional bioinformatics treats DNA codons as simple chemical markers. This device treats them as a **6-bit binary computer**. 

* **The Hexagram Mapping:** Each of the 64 codons is mapped 1:1 to an I-Ching hexagram ($2^6$).
* **Binary State:** We transition from the "Conductive" ground state (e.g., `UUU` / `000000`) to the "Active" manifestation vectors.
* **The Euler Loom:** The sequence is processed not as a string, but as a multi-dimensional lattice where each hexagram represents a specific "tension" in the W-dimension.

## 2.0 Identifying the "Null Point"
The core utility of the `potential_detector_64` script is the location of the **Null Point**. 

In high-tolerance machining, the "null" is your zero-datum. In this framework, the **Null Point** is the coordinate where the localized potential $V$ (calculated via `core_physics.py`) crosses the zero-axis. 

### Transition Manifestation
As seen in the initial v1.0 mapping:
* **Index 0-9:** A steady "charging" of the potential (from `0.0000` to `0.7730`).
* **Index 35 (AUG):** A sharp **Topological Collapse** to `-0.2903`.

The crossing between these states is the **Null Point**. This is the "Hinge" where the sequence transitions from a "Conductive" potential into a physical protein manifestation.

## 3.0 Technical Specifications
* **Core Logic:** `src/core_physics.py`
* **Visualization:** `src/visualization.py`
* **Benchmarking:** Optimized for N52 Neodymium magnetic arrays and 8B/12B graphite-burnished conductive surfaces.
* **Version:** v1.0 (Initial 64-bit Potential Mapping Success)

## 4.0 Usage
To manifest the null points from a standard FASTA sequence:
```powershell
python potential_detector_64.py --input sequence.fasta --mode null_detect --output null_points.csv
git status

git status
