import spacy
from NLP.entityMatchers import EntityMatchers
from NLP.sectionizer import Sectionizer


class LanguageProcessor:
    def __init__(self, text):
        nlp = spacy.load('en_core_web_lg')
        self.doc = nlp(text)

        self.sectionizer = Sectionizer(self.doc)
        self.entityMatcher = EntityMatchers(self.doc, nlp)

    def getDocumentSections(self):
        return self.sectionizer.getSectionsForAnnotation()

    def getDocumentEntities(self):
        return self.entityMatcher.getMatchesForAnnotation()


# For script testing
if __name__ == '__main__':
    text = '''Admission Date:  [**2198-11-23**]              Discharge Date:   [**2198-11-27**]\n\nDate of Birth:  
    [**2135-1-8**]             Sex:   M\n\nService: MEDICINE\n\nAllergies:\nPatient recorded as having No Known 
    Allergies to Drugs\n\nAttending:[**First Name3 (LF) 45**]\nChief Complaint:\nPEA arrest\n.\n\n\nMajor Surgical 
    or Invasive Procedure:\ntemporary pacemaker placement\npermanent Pacemaker placement [**2198-11-26**]\n\n\nHistory 
    of Present Illness:\nPt was in USOH, awaiting R THR, collapsed while celebrating a\nfuneral mass, was down for 1 min 
    prior to EMS arrival, found to\nbe pulseless, atrial activity noted on stips but only occasional\nwide qrs complexes, 
    could not transcut pace, got atropine and\ncalcium gluc, went to [**First Name4 (NamePattern1) 46**] [**Last Name 
    (NamePattern1) **], was intubated for protection, K\n6.6, HCO3 13, and Cr 2.7. Got kayexylate, bicarb gtt, lasix, 
    and\nextubated. ECG w/RBBB, LAD, LAFB, and sig PR delay so sent here\nfor pacer. R IJ pacer wire screwed in but still 
    temporary.\nTransferred to [**Hospital1 18**] for permanent pacer and further managment.\n\nPast Medical History:\nPMH: 
    HTN, dyslipidemia, CRI (not formally dx per pt), OA w/ hip\npain awaiting R THR, h/o chronic low potassium and severe 
    HTN\nper pt\n-baseline trifasicular block\n\nSocial History:\nPt is a priest\n\n\nFamily History:\nnon-contributory\n
    \nPhysical Exam:\nt 98.9\nBP 131/79\nHR 64\nTele: v-paced/ few PVC's with compensatory pauses\nO2 sat 92%RA\nGen: 
    elder male, lying in bed, NAD\nHEENT: JVP flat, MMM, PERRLA, EOMI\nHeart: s1, s2, RRR. no MRG\nLungs: bibasilar crackles,
     otherwise, CTAB\nExt: 1+ pedal edema bilat\nNeuro: A&O x3\n\nPertinent Results:\n[**2198-11-23**] 05:40PM   PT-14.2* 
     PTT-26.9 INR(PT)-1.4\n[**2198-11-23**] 05:40PM   PLT COUNT-137*\n[**2198-11-23**] 05:40PM   WBC-11.0 RBC-4.23* HGB-13.2*
      HCT-37.5* MCV-89\nMCH-31.1 MCHC-35.2* RDW-13.9\n[**2198-11-23**] 05:40PM   GLUCOSE-111* UREA N-55* CREAT-2.6* SODIUM-141
      \nPOTASSIUM-4.7 CHLORIDE-102 TOTAL CO2-31 ANION GAP-13\n[**2198-11-27**] 09:00AM BLOOD WBC-6.5 RBC-4.38* Hgb-13.6* 
      Hct-38.2*\nMCV-87 MCH-31.0 MCHC-35.5* RDW-13.4 Plt Ct-155\n.\nEcho [**2198-11-26**]\nConclusions:\nThere is moderate 
      symmetric left ventricular hypertrophy. The\nleft ventricular cavity size is normal. There is mild regional\nleft 
      ventricular systolic dysfunction. Resting regional wall\nmotion abnormalities include inferior and inferolateral
      \nakinesis/hypokinesis. Right ventricular chamber size and free\nwall motion are normal. The aortic valve leaflets 
      are mildly\nthickened. Mild (1+) aortic regurgitation is seen. The mitral\nvalve leaflets are mildly thickened. There 
      is a\ntrivial/physiologic pericardial effusion.\n\nCompared with the report of the prior study (tape unavailable\nfor review) 
      of\n[**2193-4-18**], left ventricular dysfunction is new and mild aortic\nregurgitation\nis now detected.\n\nBrief Hospital 
      Course:\nA/P: 63 yo male with cardiac arrest [**3-7**] paroxysmal high degree\nAV block, s/p collapse with PEA arrest now with 
      temp pacer\ntransferred to [**Hospital1 **] for further mgmt and permanent pacemaker\nplacement.\n.\n1. Rhythm: paroxysmal high 
      degree block, temp pacer placed.\nreasons for initial collapse are unclear, possibly combination\nof high degree av block and 
      electrolyte disturbances, since\npatient was on many K+sparing diuretics.  Tele after admission\nshowed V-paced with few PVCs.  
      Pt underwent pacemaker placement\non [**2198-11-26**] without complications.  The next day device\ninterrigation was satisfacotory. 
       CXR did not show a\npneumothorax or any acute processes.  Pt remained without\ncomplaints and was discharged on [**2198-11-27**].  
       Indications for\npacer was symptomatic with high degree block.\n.\n2. Coronaries: risk factors, [**Location (un) 47**] risk 17%, 
       ruled out for\nMI w/trop leak but flat CKs after arrest. -Cont ASA, BB, statin\n- lipids checked : total chol 122, HDL 36, LDL 68.  
       Continued on\nlipitor 20.\n- initially held ACEI given [**Doctor First Name 48**] upto Creatinine of 2.2.  Given\nhis hyperkalemia 
       on presentation pt was not restarted on ACE\ninhibitors as his BP was well controlled.\n- Repeat Echo (see below) showed EF of 50%.
         Given this event\nwould recommend an outpatient evaluation by cardiologist for\nlikely exercise stress test.\n.\n3. Pump: 
         EF [**2193**] was 60% w/LAE, likely diastolic dysfunction,\nmild hypervolemia w/?mild pulm edema causing
          mild hypoxia,\ninitially gentle diuresis with goals -500cc to -1L.\n- Continued amlodipine and metoprolol for 
          rate control\n- held ace/arbs due to [**Doctor First Name 48**]\n- echo [**11-26**] showed EF of 50%.\n- During 
          the admission pt did not go onto complain any further\nof Chest pain or Shortness of breath.\n.\n4. ARF/CRI: 
          acute insult likely combo of triamterene and NSAIDS,\naggrevated by diuretics and ACE-I. Baseline 1.3-1.5 with
          \nproteinuria long standing, should avoid NSAIDS for life.\n-Discontinued ACE-I/ARBa and diuretics.\n-Checked 
          FeUrea, FeUrea: 36.5%, confirming ATN. spep and upep\n(given anemia, pending), had u/s at [**Hospital1 46**] but 
          should have\nrepeat as outpt to check complex cysts vs masses. Renal diet.\n.\n5. Anemia: new,  SPEP was negative, 
          UPEP negative for bence\n[**Doctor Last Name 49**] proteins,  and iron, shows anemia likely due to renal\ncauses\n-PCP 
          may consider [**Name9 (PRE) 50**] as outpt given pt's age and anemia.\n.\n6. Thombocytopenia: new, mild and stable 
          during the admission.\n.\n7. Elevated glucose: possibly continued stress response, check\nFS wnl.\n.\n8. h/o 
          hypokalemia:  PCP may consider Nephrologist follow up.\nWould Recommend outpt mineralocorticoid XS work-up once off 
          K\nsparing diuretics for a while.\n.\n9. Hip pain: awaiting THR. vicodin prn. No NSAIDs due to renal\nproblems.\n\n10. 
          Communicate with friend, preferred HCP per pt, [**Name (NI) 51**]\n[**Name (NI) 52**] [**Telephone/Fax (1) 53**] and 
          PCP [**Name9 (PRE) 54**] [**Hospital1 18**] [**Location (un) 55**]\n[**Telephone/Fax (1) 56**]\n\n\n\nMedications on 
          Admission:\nAmlodipine 10 mg PO DAILY\nMetoprolol 100 mg PO BID\n\n\nDischarge Medications:\n1. Oxycodone-Acetaminophen 
          5-325 mg Tablet Sig: 1-2 Tablets PO\nQ4-6H (every 4 to 6 hours) as needed for pain.\nDisp:*20 Tablet(s)* Refills:*0*\n2. 
          Acetaminophen 325 mg Tablet Sig: One (1) Tablet PO Q4-6H\n(every 4 to 6 hours) as needed.\n3. Aspirin 81 mg Tablet, 
          Chewable Sig: One (1) Tablet, Chewable\nPO DAILY (Daily).\nDisp:*30 Tablet, Chewable(s)* Refills:*0*\n4. Amlodipine 5 mg 
          Tablet Sig: Two (2) Tablet PO DAILY (Daily).\nDisp:*30 Tablet(s)* Refills:*0*\n5. Atorvastatin 20 mg Tablet Sig: One (1) 
          Tablet PO DAILY\n(Daily).\nDisp:*30 Tablet(s)* Refills:*0*\n6. Cephalexin 250 mg Capsule Sig: One (1) Capsule PO Q6H (every
          \n6 hours) for 2 days.\nDisp:*10 Capsule(s)* Refills:*0*\n7. Toprol XL 200 mg Tablet Sustained Release 24HR Sig: One (1)\nTa
          blet Sustained Release 24HR PO once a day.\nDisp:*30 Tablet Sustained Release 24HR(s)* Refills:*0*\n\n\nDischarge Dispositio
          n:\nHome\n\nDischarge Diagnosis:\ncardiac arrest\nhigh degree heart block\nacute renal failure\nhyperkalemia\nmetabolic acido
          sis\nanemia with poor bone marrow response/insufficient production\nthrombocytopenia\nchronic renal insufficiency, stage 2-3\n
          HTN\ndyslipidemia\nosteoarthritis w/ hip pain awaiting R THR\nh/o chronic low potassium\n\n\nDischarge Condition:\ngood\n\n\nD
          ischarge Instructions:\nYou have had a pacemaker placed because of electrical block in\nyour heart. This may have been precipi
          tated by kidney failure\nand too much potassium in your blood. Do not take the\nmedications you were taking prior to this even
          t. We have\nenclosed a list of and prescriptions for your new medication\nneeds. Please take these as directed and discuss any 
          changes\nwith your primary care doctor.\n.\nYou have many risks for coronary heart disease. We feel you need\na stress test wit
          h imaging in the next month to make sure that\nyou do not have any significant need for a cardiac\ncatheterization. Until then,
           taking aspirin, your Toprol XL\n(beta blocker safe in renal failure), your lipitor, and\neventually starting your lisinopril a
           gain will protect you\nsomewhat from heart attacks.\n.\nYou must never take NSAID medications again. Your kidney disease\nmake
           s this dangerous. Avoid ibuprofen, advil, motrin, aleve,\nnaproxen, or ketoprofen. Talk with your doctor [**First Name (Titles)
            **] [**Last Name (Titles) 57**] if\nyou are unsure about any medications you are taking.\n\n\nFollowup Instructions:\n1. See y
            our primary care doctor Dr. [**Last Name (STitle) 58**] on Friday 28th at\n2:30pm, to check your potassium and creatinine leve
            ls and to\ndiscuss everything we recommended. Have your doctor follow up on\nthe serum and urine protein electrophoresis that 
            was pending\nwhen you were discharged as well as the final report of your\nechocardiogram. Talk with your doctor about your an
            emia and\nwhether or not you would need a bone marrow biopsy.\n\n2. Go to the pacemaker DEVICE CLINIC Phone:[**Telephone/Fax (
                1) 59**]\nDate/Time:[**2198-12-3**] 11:30\n\n3. You should see our nephrologists sometime for your kidney\ndisease. Talk 
                with your primary doctor about this and call for\nan appointment [**Telephone/Fax (1) 60**].\n\n4. You should also setup 
                an appointment with a cardiologist to\nhave a exercise stress test done as outpatient.  You can speak\nwith your PCP regar
                ding [**Name Initial (PRE) **] cardiologist or you can call [**Hospital 61**] at [**Telephone/Fax (1) 62**] to setup an a
                ppointment here.\n\n\n                             [**First Name8 (NamePattern2) **] [**Last Name (NamePattern1) **] MD [
                    **Doctor First Name 63**]\n\nCompleted by:[**2198-11-28**]'''
    lp = LanguageProcessor(text)
    print(lp.getDocumentSections())
    print(lp.getDocumentEntities())
