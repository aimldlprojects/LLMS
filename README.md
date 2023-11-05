# LLMS

Descriptive Part:
"As a medical analyst and a doctor, I need to generate detailed narratives for a set of patient data, including treatments, drugs administered, reactions, patient height, weight, MedDRA codes related to drugs and treatment, and the primary consultant's report. Each patient's data is crucial for assessment, and we require comprehensive narratives for further analysis."

Template: 
---
Patient Data:
- Patient Weight: {patientweight}
- Patient Height: {patientheight}
- Patient Gender: {patientsexr3}
- Patient Drug Name: {patientdrugname}
- Patient Invented Name: {patientinventedname}
- Primary Source Reactions Reported Language: {primarysrcreactreportedlang}
- Primary Source Reactions Native Language: {primarysrcreactinnativelang}
- Reaction MedDRA LLT: {reactionmeddrallt}
- Primary Source Reactions Native Language 1: {primarysrcreactinnativelang1}
- Reaction MedDRA LLT 1: {reactionmeddrallt1}
- Seriousness of Death: {seriousnessdeath}
- Seriousness of Life-Threatening: {seriousnesslifethreatening}
- Seriousness of Hospitalization: {seriousnesshospitalization}
- Seriousness of Disabling: {seriousnessdisabling}
- Seriousness of Congenital Anomaly: {seriousnesscongenitalanomali}
- Test Name: {testname}
- Test Name LLT: {testnamellt}
- Test Result Code: {testresultcode}
- Test Result Text: {testresulttext}
- Low Test Range: {lowtestrange}
- High Test Range: {hightestrange}
- Medicinal Product: {medicinalproduct}
- Drug Invented Name: {druginventedname}
- Drug Scientific Name: {drugscientificname}
- Drug Structure Dosage Number: {drugstructuredosagenumb}
- Drug Structure Dosage Unit: {drugstructuredosageunit}
- Drug Interval Dosage Unit Number: {drugintervaldosageunitnumb}
- Drug Indication Primary Source: {drugindicationprimarysource}
- Drug Indication MedDRA Code: {drugindicationmeddracode}
- Clinical Narrative: {narrativeincludeclinical}
---
Submitted Narrative:
"{narrativeincludeclinical}"
