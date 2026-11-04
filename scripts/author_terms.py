"""Curated, visually checked PDF quotations. No runtime extraction or paraphrasing.

All pages were rendered and reviewed for this glossary. Whitespace is reflowed;
source grammar, spelling and punctuation are retained. Formula layout is linearized.
Run from the project root to regenerate the independent glossary and its inventory.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK = json.loads((ROOT / 'data/questions.json').read_text(encoding='utf8'))
entries = {}


def add(topic, key, term, text, pages, source='methods', aliases=(), label=None):
    eid = f'{topic}-{key}'
    entry = entries.setdefault(eid, {'id': eid, 'topic': topic, 'term': term,
                                   'aliases': list(aliases), 'definitions': [], 'details': []})
    for alias in aliases:
        if alias not in entry['aliases']:
            entry['aliases'].append(alias)
    ref = {'sourceId': source, 'pages': pages}
    # Only exactly repeated wording is combined; distinct source versions remain visible.
    match = next((d for d in entry['definitions'] if d['text'] == text and d.get('label') == label), None)
    if match:
        match['sources'].append(ref)
    else:
        definition = {'text': text, 'sources': [ref]}
        if label:
            definition['label'] = label
        entry['definitions'].append(definition)
    return entry


def detail(entry, label, text, pages, source='methods', **extra):
    entry['details'].append({'label': label, 'text': text,
                             'sources': [{'sourceId': source, 'pages': pages}], **extra})


def clarify(entry, question_id):
    # Reuse already verified references, without altering the scored question bank.
    q = next(q for q in BANK['questions'] if q['id'] == question_id)
    entry['clarification'] = q['clarification']


# Foundations: exact visual text, including the source spelling EMPERICAL.
research = add('foundations', 'research', 'Research',
    'Research is an ORGANIZED and SYSTEMATIC way of FINDING ANSWERS to QUESTIONS', [17])
for label, text in [
    ('Good (1972)', 'Research is a careful, critical, disciplined inquiry, varying in techniques and methods according to the nature and conditions of the problem, directed towards clarification or resolution of the problem (Good,1972 )'),
    ('Manuel and Medel (1976)', 'Research is a process of gathering data or information to solve a particular or specific problem in a scientific manner (Manuel and Medel,1976 )'),
    ('Treece and Treece (1973)', 'Research is an attempt to gain solution to the problems, a collection of data in a rigorously controlled situation for the purpose of prediction or explanation (Treece and Treece, 1973)'),
    ('Sanchez (1980)', 'Research is a systematic study or investigation of something for the purpose of answering questions posed by the researcher (Sanchez, 1980)'),
]:
    add('foundations', 'research', 'Research', text, [17], label=label)
add('foundations', 'research', 'Research',
    'Research is a mobilizing force, not just an academic prerequisite.', [2], 'architecture')
detail(research, 'The Method / The Action / The Output',
    'The Method\nSystematic, disciplined, scientific, and empirical inquiry.\n\nThe Action\nSearching, validating, refining, and generating.\n\nThe Output\nObjective knowledge, truth, and evidence.\n\nTo mobilize society, inform action, and translate into policy/practice.', [2], 'architecture')
add('foundations', 'importance', 'Importance of Research',
    'To serve man and provide a good life\nDiscover more facts about unknown phenomena\nFind answer to the problems by existing methods and information\nImprove existing techniques and develop new instruments or products\nDiscover unrecognized substance\nDiscover pathways of action\nOrder related, valid generalization into systematized science\nProvide basis for decision making\nTo satisfy researcher’s curiosity\nTo find answers to queries\nAcquire better and deeper understanding\nTo expand and verify existing knowledge\nImproves efficiency, efficacy and quality\nImproves exportations of goods\nRespond to economic recovery & austerity', [18])
for key, term, text in [
    ('empirical', 'Empirical', 'Direct experience or observation'),
    ('logical', 'Logical', 'Valid procedure and principles'),
    ('cyclical', 'Cyclical', 'Starts with problem & ends with problem'),
    ('analytical', 'Analytical', 'Utilizes proven analytical procedures'),
    ('critical', 'Critical', 'Exhibits careful and precise judgment'),
    ('methodical', 'Methodical', 'Uses systematic method and procedures'),
    ('replicability', 'Replicability', 'Repeated to arrive at valid and conclusive results'),
]:
    add('foundations', key, term, text, [19], aliases=['EMPERICAL'] if key == 'empirical' else (),
        label='EMPERICAL' if key == 'empirical' else None)
for key, term, text in [
    ('controlled', 'Controlled', 'Minimizes effects of extraneous variables.'),
    ('transparent', 'Transparent', 'Methods, assumptions, and data are stated explicitly.'),
    ('critical', 'Critical', 'Withstands scrutiny and actively questions its own claims.'),
    ('rigorous', 'Rigorous', 'Procedures are relevant, appropriate, and justified.'),
    ('systematic', 'Systematic', 'Follows a logical sequence; deliberate and planned.'),
    ('valid-verifiable', 'Valid & Verifiable', 'Findings are correct and reproducible by others.'),
    ('empirical', 'Empirical', 'Rooted in hard evidence and real-life observation'),
]:
    add('foundations', key, term, text, [3], 'architecture')
add('foundations', 'researcher-qualities', 'Qualities of Good Researcher',
    'Research oriented\nEfficient\nScientific\nEffective\nActive\nResourceful\nCreative\nHonest\nEconomical\nReligious', [20], aliases=['RESEARCHER'])
add('foundations', 'classification', 'Classification of Research',
    'PURPOSE\nPredictive Research\nDirective Research\nIlluminative Research\n\nGOAL\nBasic or Pure Research\nApplied Research\n\nLEVELS OF INVESTIGATION\nExploratory\nDescriptive\nExperimental\n\nTYPE OF ANALYSIS\nAnalytic\nHolistic\n\nSCOPE\nAction Research\n\nCHOICE OF ANSWER\nEvaluation\nDevelopmental\n\nSTATISTICAL CONTENT\nQuantitative\nNon-Quantitative\n\nTIME ELEMENT\nHistorical\nDescriptive\nExperimental', [21])
add('foundations', 'professional-goals', 'Professional Goals',
    'Produce evidence-based practice\nEstablish professional credibility\nObserve accountability for actions\nPromote cost-effectiveness via documentation', [4], 'architecture')

# Variables and processes.
variable = add('variables', 'variable', 'Variable',
    'Defined as quantity susceptible of fluctuations of change in value or magnitude under different conditions (Calmorin, 2007)', [22])
add('variables', 'variable', 'Variable',
    'A quality or characteristics that two or more mutually exclusive values or properties ( Sevilla et. All, 2002)', [22])
for key, term, text in [
    ('independent', 'Independent Variable', 'This is a stimulus variables which chosen by the researcher to determine its relationship to an observe phenomena'),
    ('dependent', 'Dependent Variable', 'This is a response variable which is observed and measured to determine the effect of the independent variables.'),
    ('intervening', 'Intervening Variable', 'This variable intrudes or interferes with the IV and DV but its effects can either reinforce or weaken the IV and DV.'),
    ('control', 'Control Variable', 'This variable controlled by the researcher in which the effects can be neutralized by eliminating or removing the variable.'),
    ('moderator', 'Moderator Variable', 'This is secondary or special type of variable chosen by the researcher to determine if it alters or modifies the relationships between the independent and dependent variables.'),
]:
    entry = add('variables', key, term, text, [23], aliases={'independent':['IV'],'dependent':['DV']}.get(key, []))
    if key == 'independent':
        detail(entry, 'Examples', 'Mathematics Scores and Number of Hours Study in Mathematics as Perceived by Sophomore Secondary Students in Private Schools in Cebu City\n\nNumber of Hours → Age, gender, socio-economic, attitudes towards study → Mathematics scores\n\nWeight Increment of Grouper Cultured in Fish Cages using Pellets and Bread Meal as Supplemental Feeds.\n\nPellets of Bread Meal → Salinity Oxygen Temperature, ph → Weight Increment', [24])
process = add('variables', 'process', 'Research Process',
    '1 PROBLEM/OBJECTIVES\n2 THEORITICAL/CONCEPTUAL FRAMEWORK\n3 ASSUMPTIONS\n4 HYPOTHESIS\n5 REVIEW OF RELATED LITERATURE\n6 RESEARCH DESIGN\n7 DATA COLLECTION\n8 DATA PROCESSING\n9 STATISTICAL TREATMENT\n10 ANALYSIS & INTERPRETATION\n11 SUMMARY/CONCLUSION/RECOMMENDATION', [25])
detail(process, 'The Research Process — flowchart labels',
    'Identification and Definition of a Research Problem\nStatement of Research Problem/Objectives\nTheoretical/Conceptual Framework Formulation\nOperational Definition of Variables\nHypothesis Formulation\nChoosing Appropriate Research Design\nIdentification of Target Population and Sampling\nData Collection\nPreparation of Research Instrument\nReliability Testing and Validation\nQ Administration, Interview, Testing & Observation\nQuality Control\nData Processing\n(Editing, Coding, Encoding, Creation of Data Files Tabulation)\nData Analysis and Interpretation\n(Statistical Analysis, Interpretation, Generalization)\nReport Preparation and Information Dissemination', [26])

# Research problems, objectives, and title guidance.
problem = add('problems', 'research-problem', 'Research Problem',
    'Problem is any (1) significant, perplexing and challenging situation, real or artificial, the solution of which requires reflective thinking (2) a perplexing situation after it has been translated into a question or series of questions that help determine the direction of subsequent inquiry Dewey as cited by Good ( ).', [31,32])
add('problems', 'research-problem', 'Research Problem',
    'A problem that someone would like to research. A problem that a person finds unsatisfactory or unsettling, a difficulty of some sort, a state of affairs that needs to be change.', [31,32])
detail(problem, 'Characteristics of Research Problem', 'Novelty\nInteresting\nRelevant\nFeasible\nResearchable (SMART)\nEthical\nSystematic', [34])
detail(problem, 'Sources of Research Problems (Calmorin & Calmorin, 2007)',
    'Specialization of the researcher\nThe field of speicalization of the researcher is an impetus towards conduct of research\n\nCxurrent and Past Researches\nCurrent and past are rich sources of RP\n\nRecommendations from Theses and research journals\n\nOriginal and creative ideas of the researcher based on problems met in locality', [35])
detail(problem, 'Guideline in the selection of research problem',
    'The research problem or topic must be chosen by the researcher himself.\nIt must be within the interest of the researcher.\nIt must be within the specialization of the researcher.\nIt must be within the competence of the researcher to tackle.\nIt must be within the ability of the researcher to finance; otherwise he must be able to find funding for research.\nIt is researcher and manageable that is,', [36])
for key, term, text in [
    ('why', 'WHY?', 'Aim or purpose of the problem for investigation'),
    ('what', 'WHAT?', 'The subject matter or topic to be investigated.'),
    ('where', 'WHERE?', 'The place or locale where the research is to be conducted.'),
    ('when', 'WHEN?', 'The period or time of the study during the data are to be gathered.'),
    ('who', 'WHO?', 'Population or universe from whom the data are to be collected'),
]:
    add('problems', key, term, text, [33])
statement = add('problems', 'statement-objectives', 'Statement of Research Problem/Objectives',
    'Research problem and research objectives have the same characteristics but they differ in form because the former is stated in interrogative or question form and the latter, in declarative form.', [41], aliases=['research objectives','statement of the problem'])
detail(statement, 'Formulating research problem',
    'The general statement of the problem and the specific sub-problems or questions should be formulated first before conducting the research.\nIt is customary to state specific sub-problems (specific questions) in the interrogative form.\nEach specific questions must be clear and unequivocal (one meaning)\nEach specific question is researchable apart from the other questions, which are answers to specific questions can be found even without considering the other questions.\nEach question must be based upon known facts and phenomena.\nAnswers to each specific question can be interpreted apart from the answers to other specific questions.\nAnswers to each specific question must contribute to the development of the whole research problem or topic.\nSumming up the answers to all specific questions will give a complete development of the entire study\nThe number of specific questions should be enough to cover the development of the whole research problem or study.\nThere should be a general statement of the problem and then should be broken up into as many sub-problems or specific questions as necessary', [37])
add('problems', 'research-title', 'Research Title',
    'It must grab the attention and makes you want to read further\nIt must be intriguing, thought-provoking\nIt must include the 5Ws\nIt must be brief and concise with a maximum of 20 words and writen in inverted pyramid and in capital letters\nIt must avoid a study of, an investigation of , an analysis,,,\nIt must follow the format required by institution.', [38])

# Frameworks and definitions: selectable text checked against rendered slides.
for key, term, text, pages in [
    ('hypothesis', 'Hypothesis', 'is defined as a wise guess that is formulated and temporarily adopted to explain the observed facts covered by the study.', [42]),
    ('null', 'Null Hypothesis', 'is a denial of an existence of a trait, characteristic, quality, value, correlation or difference of the result.', [42]),
    ('alternative', 'Alternative Hypothesis', 'is an affirmation of the existence of the observed phenomenon.', [42]),
    ('theoretical', 'Theoretical Framework', 'shapes the justification of the research problem/research objectives in order to provide the legal basis for defining its parameters', [43]),
    ('conceptual-framework', 'Conceptual Framework', 'presents specific and well-defined concepts which are called constructs.', [44]),
    ('assumptions', 'Assumptions', 'are presumed to be true statements of facts related to the research problem.', [45]),
    ('significance', 'Significance of the Study', 'Is presented comprehensively to convince the screening committee the importance of the study.', [46]),
    ('scope', 'Scope and Limitations of the Study', 'This includes the coverage of the study area, the subjects, the research apparatus, equipment or instrument, the research issues and concerns, the duration of the study, and the constraints that have direct bearing on the result of the study.', [47,49]),
    ('conceptual-definition', 'Conceptual Definition', 'The definition are based on concepts or hypothetic ones which are usually taken from a dictionary, encyclopedia and published journals.', [48]),
    ('operational-definition', 'Operational Definition', 'The definition of terms are based on observable characteristics and how it is used in the study.', [48]),
]:
    e = add('frameworks', key, term, text, pages)
    if key == 'theoretical':
        clarify(e, 'frameworks-theoretical')
add('frameworks', 'conceptual-definition', 'Conceptual Definition',
    'also known as constitutive, is that which is given in dictionaries. It is the academic or universal meaning attributed to a word or group of works. Moreover, it is mostly abstract and formal in nature.', [67], aliases=['constitutive'])
add('frameworks', 'operational-definition', 'Operational Definition',
    'also known as functional. Operational definition may be measured and experimental. The measured operational definition states the way the concept is measured in the investigation. In an experimental operational definition the researcher may spell out the details of the manipulation of a variable.', [68], aliases=['functional'])

# Instruments.
for key, term, text in [
    ('validity', 'Validity', 'It means the degree to which a test or measuring instrument measures what it intends to measure.'),
    ('content-validity', 'Content validity', 'It means the extent to which the content or topics of the test is truly representative of the content of the course.'),
    ('concurrent-validity', 'Concurrent validity', 'It is the degree to which the test agrees or correlates with a criterion set up as an acceptable measure.'),
    ('predictive-validity', 'Predictive validity', 'It is determined by showing how well predictions made from the test are confirmed by evidence gathered at some subsequent time.'),
    ('construct-validity', 'Construct validity', 'It is the extent to which the test measures a theoretical construct or trait.'),
]:
    add('instruments', key, term, text, [27])
add('instruments', 'reliability', 'Reliability', 'It means the extent to which a research instrument is dependable, consistent and stable.', [28])
add('instruments', 'usability', 'Usability', 'It means the degree to which the research instrument be satisfactorily used by teachers, researchers, supervisors and school managers without expenditures of time, money and effect.', [29])
for key, term, text in [
    ('administration', 'Base of administration', 'To facilitate the administration of a research instrument, instruction should be complete and precise.'),
    ('scoring', 'Base of scoring', 'It depends on the following aspects:\nConstruction of a test in the objective type.\nAnswer keys are adequately prepared.\nScoring directions are fully understood.'),
    ('interpretation', 'Ease of interpretation and application', 'Results of test are easy to interpret and apply if tables are provided.'),
    ('cost', 'Low cost', 'It is more practical if the test is low cost material-wise.'),
    ('mechanical', 'Proper mechanical make-up', 'A good research instrument should be printed clearly in an appropriate size for the grade or year level for which the instrument is intended.'),
]:
    add('instruments', key, term, text, [29])

# Literature and studies.
literature = add('literature', 'related-literature', 'Related Literature',
    'Related literature is composed of discussions of facts and principles to which the present study is related.\n\nThe materials are usually printed and found in books, encyclopedias, professional journals, magazines, newspapers, and other publications.', [51])
add('literature', 'related-literature', 'Related Literature',
    'It is a section in a research paper, thesis dissertation, and research project in which the sources are taken from books, journals, magazines, novels, poetry, etc that contains facts, laws, theories and other documented observations. This is in a chronological order from recent to past when presented. It is unscientific if related literature are presented and of no explanation at the relevance to the present study.', [63])
detail(literature, 'Importance, purpose and functions',
    'Reviewed literature and studies help or guide the researcher in the following ways:\nHelp or guide the researcher in searching for or selecting a better research problem or topic.\nHelp the investigator understand his topic for research better.\nEnsure that there will be no duplication of other studies.\nHelp and guide the researcher in locating more sources of related information.\nHelp and guide the researcher in making his research design especially in\na. The formulation of specific questions to be researched on;\nb. The formulation of assumptions and hypotheses if there should be any;\nc. The formulation of conceptual framework;\nd. The selection and application of the methods of research;\ne. The selection and application of sampling technique;\nf. The selection and/ or preparation and validation of research instruments for gathering data;\ng. The selection and application of statistical procedures;\nh. The analysis, organization, presentation, and interpretation of data;\ni. The making of the summary of findings, conclusions, and recommendations; and\nHelp and guide the researcher in making comparison between his findings with the findings of other researchers on similar studies with the end in view of formulating generalizations or principles which are the contributions of the study to the fund of knowledge.', [52,53,54])
detail(literature, 'Characteristics of related literature',
    'The surveyed materials must be as recent as possible\nExceptions:\nA. Treatises that deal on universals or things of more or less permanent nature may still be good today.\nB. When a comparison or contrast is to be made between the conditions of today and those of a remote past, say ten or twenty years ago.\nMaterials reviewed must be objective and unbiased.\nMaterials surveyed must be relevant to the study.\nSurveyed materials must have been based upon genuinely original and true facts or data to make valid and reliable.\nReviewed materials must not be too few or too many.', [55,56])
detail(literature, 'Sources and where to locate sources',
    'Literature reviewed typically includes scholarly journals, scholarly books, authoritative databases and primary sources. Sometimes it includes newspapers, magazines, other books, films, and audio and video tapes, and other secondary sources.\n\nGenerally, the sources of related literature and studies are located in the following places:\nLibraries, either government, school, or private libraries.\nGovernment and private offices.\nThe National Library.\nThe library of the Department of Education, Culture and Sports.\nThe last two are especially rich depositories of related materials, particularly unpublished master’s thesis and doctoral dissertations.', [57,60])
primary = add('literature', 'primary', 'Primary sources',
    'Primary sources are the origin of information under study, fundamental documents relating to a particular subject or idea. Often they are first hand accounts written by a witness or researcher at the time of an event or discovery.', [58])
detail(primary, 'Examples as printed on the slide', 'E.g. published books, magazines, encyclopedias, almanacs and etc.', [58])
clarify(primary, 'literature-primary-examples-slide')
secondary = add('literature', 'secondary', 'Secondary sources',
    'Secondary sources are documents or recordings that relate to or discuss information originally presented elsewhere.', [59])
detail(secondary, 'Examples as printed on the slide', 'E.g. Information from the internet, unpublished thesis and dissertations', [59])
clarify(secondary, 'literature-secondary-examples-slide')
legal = add('literature', 'legal', 'Related Legal Bases',
    'Related – means the legal bases, literature and studies which have direct bearing or relation to the present study.\n\nIt determine the relevance of the study to the government’s thrusts. The major sources of related legal bases are laws and department directives such as circulars, orders, memoranda, and others which are related to the present study.', [61])
studies = add('literature', 'related-studies', 'Related Studies (Local or Foreign)',
    'Published and unpublished research studies are sources of materials that are included in this section. The research studies which have direct bearing to the present study are segregated into foreign and local studies.', [65], aliases=['local studies','foreign studies'])
# These are examples of literature/studies, not new general definitions of nursing concepts.
for entry, page, label in [(legal,62,'Example and explanation of the legal basis'),(literature,64,'Example and explanation of the related literature'),(studies,66,'Example of local study')]:
    # Selectable text was compared with the rendered page; remove only slide bullet glyphs/heading.
    import re
    import pymupdf
    with pymupdf.open(ROOT / 'pdfs/methodsofresearch1.pptx.pdf') as doc:
        raw = doc[page-1].get_text(sort=True)
    raw = raw.replace('⦿','').strip()
    text = '\n\n'.join(' '.join(part.split()) for part in raw.split('\n\n') if part.strip())
    detail(entry, label, text, [page])

# Research designs and their constituent concepts.
design = add('designs', 'research-design', 'Research Design',
    'Task of defining the research problem is the preparation of the research project, popularly known as the “research design”.\nDecisions regarding what, where, when, how much, by what means concerning an inquiry or a research study constitute a research design.', [70])
for text in [
    'A research design is the arrangement of conditions for collection and analysis of data in a manner that aims to combine relevance to the research purpose with economy in procedure.',
    'Blueprint of the study. It guides the collection, measurement and analysis of data',
    'A plan or structure of the investigation in order to obtain answers to research questions. It outline what the researcher would like to do until the final analysis of the data',
]:
    add('designs', 'research-design', 'Research Design', text, [71])
detail(design, 'Features of Good RS',
    'A research design appropriate for a particular research problem, usually involves the following features.\nThe mean of obtaining information.\nThe availability and skills of the researcher and his staff, if any.\nThe objective of the problem to be studied.\nThe nature of the problem to be studied .\nThe availability of time and money for the research work.', [73])
for key, term, text in [
    ('sampling', 'Sampling Design', 'Which deals with the methods of selecting items to be observed for the study.'),
    ('observational', 'Observational design', 'Which relates to the condition under which the observation are to be create'),
    ('statistical', 'Statistical Design', 'Which concern the question of the of How the information and data gathered are to be analyzed ?'),
    ('operational', 'Operational design', 'Which deals with techniques by which the procedures satisfied in sampling .'),
]:
    add('designs', key, term, text, [72])
add('designs', 'research-hypothesis', 'Research hypothesis', 'The researcher hypothesis is a predicative statement that relates an independent variable to dependent variable.', [75])
testing = add('designs', 'hypothesis-testing', 'Hypothesis-testing research',
    'When the purpose of research is to test a research hypothesis, it us termed as hypothesis testing research .It can be experimental or non-experimental', [75])
add('designs', 'hypothesis-testing', 'Hypothesis-testing research',
    'hypothesis-testing research studies known as experimental studies are those researcher tests the hypothesis of casual relationship between variables.', [76])
for key, term, text in [
    ('control-group', 'Control group', 'When a group is exposed to usual conditions, it is termed as a control group.'),
    ('experimental-group', 'Experimental group', 'But when the group is exposed to be some special condition, it is termed as Experimental group'),
    ('treatments', 'Treatments', 'The different conditions under which Experiment and control groups are put up usually referred to as treatment.'),
    ('experiment', 'Experiment', 'The process of examining the truth of a statistical hypothesis, relating to some research problem, is known as an Experiment.'),
]:
    add('designs', key, term, text, [75])
explore = add('designs', 'exploratory', 'Exploratory research',
    'exploratory research method are also termed as formulative research studied.\nThe main purpose is that of formulate the research problem .three methods are\n1. The survey of concerning literature\n2. The experience survey\n3. The analysis of ‘inside-stimulating', [76], aliases=['formulative research'])
add('designs', 'exploratory', 'Exploratory research', 'Formulating precise questions; navigating the unknown.', [4], 'architecture')
detail(explore, 'Formulative design comparison', 'Flexible design\nJudgmental sampling\nNo pre-determined design\nNo fixed decision about the operational procedures', [77])
diagnostic = add('designs', 'diagnostic', 'Diagnostic research', 'In diagnostic research study determine the frequency which some thing occur', [76])
detail(diagnostic, 'Descriptive/diagnostic design comparison', 'No flexibility\nRandom sampling\nPre-determined design for analysis\nAdvanced decisions', [77])
add('designs', 'explanatory', 'Explanatory', 'Identifying underlying causes and reasons (the ‘Why’).', [4], 'architecture')
quasi = add('designs', 'quasi-experimental', 'Quasi-experimental', 'Test for cause/effect relationships without full control', [78])
detail(quasi, 'Research Designs/Approaches — table row', 'Time frame\nCurrent or past\n\nDegree of control\nModerate to high\n\nExamples\nGender differences in visual/spatial abilities', [78])
clarify(quasi, 'designs-quasi-example')
nonexperimental = add('designs', 'non-experimental', 'Non-Experimental', 'Relies on variables that cannot be manipulated (gender, ethnicity, etc.).\nTypes: Action, Comparative, Developmental, Evaluation, Meta-analysis, Survey.', [9], 'architecture')
correlation = add('designs', 'non-experimental-correlational', 'Non-experimental - correlational', 'Examine relationship between two variables', [78])
add('designs', 'non-experimental-correlational', 'Non-experimental - correlational', 'Examine relationship bet 2 var. where 1 is measured later.', [79])
detail(correlation, 'Research Designs/Approaches — page 78', 'Time frame\nCurrent (cross-sectional) or past\n\nDegree of control\nLow to medium\n\nExamples\nRelationship between studying style and grade point average.', [78])
detail(correlation, 'Research Designs/Approaches — page 79', 'Time frame\nFuture - predictive\n\nDegree of control\nLow to moderate\n\nExamples\nRelationship bet history of depression & development of cancer.', [79])
add('designs', 'ex-post-facto', 'Ex post facto', 'Examine the effect of past event on current functioning.', [78])
cohort = add('designs', 'cohort-sequential', 'Cohort-sequential', 'Examine change in a var. over time in overlapping', [79])
cohort['sourceNote'] = 'The purpose cell ends at “overlapping” in the supplied slide; no missing words have been supplied.'
detail(cohort, 'Research Designs/Approaches — table row', 'Time frame\nFuture\n\nDegree of control\nLow to moderate', [79])

# Historical sources and criticism.
history = add('historical', 'historical-research', 'Historical Research',
    'Historical Research is the systematic collection and evaluation of data to describe, explain, and thereby understand actions or events that occurred sometime in the past. (J.M. Fraenkel & N.E. Wallen)', [81])
add('historical', 'historical-research', 'Historical Research',
    'Examines past events to anticipate future effects. Relies on Primary (eyewitness) and Secondary sources. Must pass internal and external criticism.', [11], 'architecture')
detail(history, 'Characteristic, advantages and disadvantages',
    'The unique characteristic of historical research is that it focuses exclusively on past occurrences and events. (J.M. Fraenkel & N.E. Wallen)\n\nAdvantages\nIt is the only research method that can study evidence from the past.\nWider range of evidence than most other methods.\n\nDisadvantages\nThe measures used in other methods to control for threats to internal validity are simply not possible in a historical study.\nBias', [81])
detail(history, 'Uses of historical research',
    '1. To make people aware of what has happened in the past so they may learn from past failures and successes.\n2. To learn how things were done in the past to see if they might be applicable to present-day problems and concerns.\n3. To assist in prediction.\n4. To test hypotheses concerning relationships or trends.', [82])
detail(history, 'Major steps of historical design', 'I. DEFINING THE PROBLEM\nII. LOCATING RELEVANT SOURCES\nIII. SUMMARIZING INFORMATION OBTAINED FROM HISTORICAL SOURCES\nIV. THE EVALUATION OF HISTORICAL SOURCES', [83,86])
for key, term, text, pages in [
    ('documents', 'Documents', 'are written or printed materials that have been produced in some form or another—annual reports, artwork, bills, books, cartoons, circulars, court records, diaries, diplomas, legal records, newspapers, magazines, notebooks, school yearbooks, memos, tests , and so on.', [83]),
    ('numerical', 'Numerical records', 'Numerical, or quantitative, records can be considered either as a separate type of source in and of themselves or as a subcategory of documents—test scores, attendance figures, census reports, school budgets, and the like.', [83]),
    ('oral', 'Oral statements', 'another valuable source of information for the historical researcher lies in the statements people make orally—stories, myths, tales, legends, chants, songs and other forms of oral; expression have been used by people down through the ages to leave a record for future generations.', [84]),
    ('relics', 'Relics', 'is any object whose physical or visual characteristics can provide some information about the past—furniture, artwork, clothing, buildings, monuments, or equipment.', [84]),
    ('primary', 'Primary Source', 'Is one prepared by an individual who was a participant in or a direct witness to the event being described.', [84]),
    ('secondary', 'Secondary Source', 'Is a documents prepared by an individual who was not a direct witness to an event, but obtained his or her description of the event from someone else.', [84]),
    ('external-criticism', 'External Criticism', 'Refers to the genuineness of any and all documents the researcher uses.', [86]),
    ('internal-criticism', 'Internal Criticism', 'Once researchers have satisfied themselves that a source document is genuine, they need to determine if the contents of the documents are accurate. This involves what is known as internal criticism. Both the accuracy of the information contained in a document and the truthfulness of the author need to be evaluated.', [87]),
]:
    add('historical', key, term, text, pages)
detail(entries['historical-primary'], 'Primary source examples',
    '1. A nineteenth-century teacher’s account of what it was like to live with a frontier family.\n2. A photograph of an eight-grade graduating class in 1930.\n3. Essays written by students in response to the question, “What do you like most and least about school?”\n4. Minutes of a school board meeting taken by the secretary of the board.\n5. Songs composed by members of a high school glee club.', [85])
detail(entries['historical-secondary'], 'Secondary source examples',
    '1. An encyclopedia describing various types of educational research conducted over a 10-year period.\n2. A magazine article summarizing Aristotle’s views on education.\n3. A student’s report to her counselor of why her teacher said she was being suspended from school.\n4. A book describing schooling in the New England colonies during the 1700s.\n5. A newspaper account of a school board meeting based on oral interviews with members of the board.', [85])
detail(entries['historical-external-criticism'], 'Questions for evaluating genuineness',
    'Who wrote this documents? Was the author living at that time?\nFor what purpose was the document written? For whom was it intended? And why?\nWhen was the document written? Is the date on the document accurate? Could the details describes have actually happened during this time?\nWhere was the document written? Could the details described have occurred in this location?\nUnder what conditions was the document written? Is there any possibility that what was written might have been directly or subtly coerced?\nDo different forms or versions of the document exist?', [86,87])
detail(entries['historical-internal-criticism'], 'With regard to the author of the document',
    'Was the author present at the event he or she is describing? In other words, is the document a primary or a secondary source?\nWas the author a participant in or an observer of the event ?\nWas the author competent to describe the event?', [87])

# Descriptive research: preserve the source's nonstandard spelling.
descriptive = add('descriptive', 'descriptive-research', 'Descriptive Research',
    'The descriptive research is the most popular approach used in research project. Derived from the Latin word de meaning from and scribe meaning write.\n\nDescriptive research includes all studies that purport to present facts concerning the nature and status of anything – a group of persons, a number of objects, a set of conditions, a class of events, a system of thought or any other kind of phenomena which one may wish to study', [89])
add('descriptive', 'descriptive-research', 'Descriptive Research',
    'Descriptive research is fact-finding with adequate interpretation. It is something more and beyond just data-gathering; the latter is not reflective thinking nor research. The true meaning of the data collected should be reported from the point of view of the objectives and basic assumption of the project underway.', [89])
add('descriptive', 'descriptive-research', 'Descriptive Research',
    'As defined by Best (1963) – Descriptive research describes and interprets what is. It is concerned with conditions of relationships that exist, practices that prevail, beliefs and processes that are going on, effects that are being felt, or trends that are developing.', [89])
add('descriptive', 'descriptive-research', 'Descriptive Research',
    'in case of descriptive research study –one those studied which are concerned with describing the characteristics of a particular Individual , or a group.', [76])
add('descriptive', 'descriptive-research', 'Descriptive Research', 'Presenting specific details (the Who, What, Where, and How).', [4], 'architecture')
detail(descriptive, 'Quantitative or qualitative descriptions — legible introductory passage',
    'Descriptive research can be either quantitative or qualitative. It can involve collections of quantitative information that can be tabulated along a continuum in numerical form, such as scores on a test or the number of times a person chooses to use a certain feature of a multimedia program, or it can describe categories of information such as gender or patterns of interaction when using technology in a group situation. Descriptive research involves gathering data that describe events and then organizes, tabulates, depicts, and describes the data collection (Glass & Hopkins, 1984). It often uses visual aids such as graphs and charts to aid the reader in understanding the data distribution. Because the human mind cannot extract the full import of a large mass of raw data, descriptive statistics are very important in reducing the data to manageable form.', [90])
for key, term, text, page in [
    ('survey', 'Descriptive Survey Method', 'Survey derived from the Latin sur or super which means “above” or “view” and vey which means “to look” or “to see”. Survey means “to look over or beyond”. Ussually used by graduate and undergraduate students when they attemp to analyze, interpret, and report status od their subject matter or problem', 92),
    ('normative', 'Descriptive Normative Method', 'Describes the status of events and people or subjects as they exist. Deals with standardized instruments like mental ability test, stress and personality questionnaire, morale and job satisfaction questionnaire.', 92),
    ('correlational', 'Descriptive Correlational Method', 'Used to determine whether or not there is a relationship that exist between two or more quantifiable variables, and if there is, to what extent or degree the relationship is determined, the researcher must identify whether such relationship is positive (+) or negative (-) and the degree or extent (strength) of relationship.', 92),
    ('evaluative', 'Descriptive Evaluative Method', 'This study judges the goodness of an existing program. It is directed to whether or not a particular program achieved its goal or not. Value judgement in terms of effectiveness, desirability, or social validity.', 92),
    ('assessment', 'Descriptive Assessment Method', 'A fact-finding activity that describes coditions that exist at a particular time such as practices and beliefs. No hypothesis are preposed or tested.', 93),
    ('trend', 'Descriptive Trend and Perspective Method', 'This descriptive research based upon longitudinal consideration of recorded data, indicating what has been happening in the past, what the present situation reveals, and on the basis of these data it projects what is likely to happen in the future.', 93),
    ('ex-post-facto', 'Descriptive Ex-Post Facto Method', 'This type of research is also known as causal-comparative research of after-the-fact research. In this method, the researcher is trying to establish a causal effect between existing conditions.', 93),
    ('case-study', 'Descriptive Case study Method', 'A case study is an intensive and descriptive analyss of a single subject. It examines a social units as a whole, and the unit may be a single typical individual. It examines a social unit as a whole, and the unit may be a single typical individual, a family, a social group, a social institution or a community', 93),
    ('comparative', 'Descriptive Comparative Method', 'This method provides an explanation about the extent of relationship between two or more variables. The researcher examines the relationships including similarities or differences among several variables.', 94),
]:
    e = add('descriptive', key, term, text, [page])
    if key == 'comparative':
        add('descriptive', key, term,
            'The researcher is knowledgeable about the operation of natural or social forceswhich maybe obtained by watching them analytically at stated intervals in their development over a long periood of time as seen desirable and possible. Also called a genetic method.', [94], label='Paragraph under the numbered heading')
        clarify(e, 'descriptive-genetic-heading')
        detail(e, 'Advantages and disadvantages of Comparative Study',
            'Advantages of Comparative Study:\nIntervening variables of comparative study can easily be noted and discerned\nResearch variables can easily be selected.\nComparative results of this study can be known immediately\nComparative method is easily conducted.\n\nDisadvantages of Comparative Study:\nThe findings of the study are very much limited because it cannot show the cause of a change in another variable.\nVariables to be selected are likewise limited.\nIt is difficult to get samples which have the same characteristics or attributes.', [94])

# Experimental definitions and plans.
experimental = add('experimental', 'experimental-design', 'Experimental Design',
    'problem solving approach that the study is described in the future on what will be when variables are carefully controlled or manipulated\n\ncan be a basic, applied, or developmental research\n\na research wherein a researcher manipulates and controls one or more independent variables for variation concomitant to the manipulation of the dependent variable\n\nused to find out what caused the change in the characteristics or behavior of the subjects and what change or effect has been made then', [96])
clarify(experimental, 'experimental-dependent-wording')
add('experimental', 'experimental-design', 'Experimental Design', 'Test for cause/effect relationships', [78])
add('experimental', 'experimental-design', 'Experimental Design', 'Guided strictly by hypotheses; involves direct manipulation and control of variables to prove or disprove statements.', [8], 'architecture')
detail(experimental, 'Distinguishing Features',
    'It is usually involves two groups - an experimental group and a control group\nExperimental group – exposed to the influence of a factor - an intervention or treatment under consideration\nControl group – not exposed to the same factor to which experimental group is exposed to, or it receives a different treatment, or it is left to its usual way of doing things\nThe control and manipulation of variables constitute the essential feature of experimental design\nThe only design wherein the invest – harvest principle can be attained.\nIt is expected to reveal cause and effect relationship even if the experiment conducted in the field or laboratory\nIt is given priority by research institutions in giving of research grants-in-aid', [97])
add('experimental', 'seven-ms', '7 Ms', 'Manpower\nMoney\nMethods\nMaterials\nMachinery\nMoment of time\nMarketing', [98])
plan = add('experimental', 'plan', 'Experimental Plan',
    '1. Determining the experimental problem or topic\n2. Surveying related literature and studies\n3. Formulating the hypothesis or hypotheses\n4. Identifying the experimental variables\n5. Select the appropriate experimental design\n6. Selecting the sample\n7. Selecting or constructing appropriate instruments to measure the results of the experiment\n8. Conducting the experiment\n   History\n   Maturation\n   Testing\n   Biases in the selection of the respondents\n   Experimental mortality\n   Interaction effects\n9. Measuring the results and applying statistical procedures\n10. Writing the reports of the experiment', [99])
for key, term, text, page, diagram in [
    ('posttest-only', 'Posttest only design', 'Also known as one shot case study\ninvolves just one group of subjects which is exposed to an intervention or treatment. After sometime it is given a posttest or is subject for observation.', 100, 'Experimental Group    X    O'),
    ('one-group-pretest-posttest', 'The one-group pretest-posttest design', 'As to posttest-only, this design is without a control group.\nHowever, a pretest or baseline observation (O1) which allows the investigator to determine the effects of the treatment by comparing pretest and posttest (O2) results.', 100, 'Experimental Group    O₁    X    O₂'),
    ('static-group', 'The static-group comparison design', 'It has a control or comparison group.\nExperimental group is exposed to an intervention or treatment (X) which is derived of the control group.\nAfter some time the experimental group and the control group are observed', 101, 'Experimental Group    X    O\nControl Group              O'),
    ('pretest-posttest-control', 'The pretest-posttest control group design', 'this design involves the random assignment of subjects from a single population the experimental and the control groups.\nthis two groups receive initial observations or pretests (O1 & O3) and posttest (O2 & O4) to determine the differences.', 101, 'R Experimental Group    O₁    X    O₂\nR Control Group         O₃         O₄'),
    ('posttest-control', 'The posttest-only control group design', 'Involves both the experimental and the control groups which were created through random assignment (R) subjects from a study population.\nboth are not given pretest; both receives posttest after the experimental group has been exposed to intervention or', 102, 'R Experimental Group    X    O₁\nR Control Group              O₂'),
    ('solomon', 'The Solomon four-group design', 'The subjects are randomly assigned to four groups.\nTwo groups are experimental and the other two groups are control groups.\nOne experimental group and one control group is subject to pretest, and all four are subject to posttest.', 102, 'R Experimental Group    O₁    X    O₂\nR Control Group         O₃         O₄\nR Experimental Group          X    O₅\nR Control Group                    O₆'),
    ('non-equivalent', 'The non-equivalent control group design', 'involves two groups which are the experimental and the control groups.\nlike pretest-posttest control group design both experimental and control group undergo pretest and posttest, the only difference is that, in this design the assignment of subjects into these groups is not done', 103, 'Experimental Group    O₁    X    O₂\nControl Group         O₃    X    O₄'),
    ('separate-sample', 'Separate Sample pretest-posttest group design', 'involves two groups, the creation of which was done by a random selection (R) of samples.\none group is subject to a baseline pretest (O1), and another group is used for the posttest measurement (O2).', 103, None),
    ('time-series', 'The time-series design', 'an improvement of the one-group pretest-posttest design because it has the advantage of repeated observations before and after the intervention or treatment has been introduced to the study group.\nthe more number of pretest and posttest the better it will be for study.', 104, 'Experimental Group    O₁ O₂ O₃ O₄ X O₅ O₆ O₇ O₈'),
]:
    e = add('experimental', key, term, text, [page])
    if diagram:
        detail(e, 'Notation as printed on the slide', '', [page], diagram=diagram)
    if key in ['posttest-control','non-equivalent']:
        e['sourceNote'] = 'The description ends at the quoted word in the supplied slide; no missing ending has been supplied.'
    if key == 'non-equivalent':
        clarify(e, 'experimental-nonequivalent-printed')
    if key == 'separate-sample':
        clarify(e, 'experimental-separate-printed')
for key, term, text in [
    ('true-experimental', 'True Experimental', 'Pretest-posttest, Solomon four-group.'),
    ('quasi-experimental', 'Quasi-experimental', 'Non-equivalent, Time series.'),
    ('pre-experimental', 'Pre-experimental', 'One-shot case, One group pretest.'),
]:
    add('experimental', key, term, text, [9], 'architecture')
internal = add('experimental', 'internal-validity', 'Internal validity', 'changes attributed to independent variable', [9], 'architecture')
external = add('experimental', 'external-validity', 'External validity', 'changes attributed to extraneous variables', [9], 'architecture')
clarify(external, 'approaches-external-validity-slide')

# Modern approaches, time dimensions and qualitative/mixed concepts.
for key, term, text, page, aliases in [
    ('basic', 'Basic Research', 'Goal: Advance fundamental knowledge.\nFocus: Refuting/supporting theories of how the world operates.\nPrimary Consumer: The academic community.', 5, ['pure research']),
    ('applied', 'Applied Research', 'Goal: Solve specific problems or accomplish tasks.\nFocus: Immediate practical use and descriptive clarity.\nPrimary Consumer: Practitioners, decision-makers, teachers.', 5, []),
    ('action', 'Action Research', 'Conducted by/for practitioners to immediately refine their own actions.', 6, []),
    ('impact', 'Impact Assessment', 'Estimating the consequences of a planned change or policy.', 6, []),
    ('evaluation', 'Evaluation', 'Establishing value judgments (Formative = ongoing monitoring; Summative = final outcomes).', 6, ['formative','summative']),
    ('cross-sectional', 'Cross-Sectional', 'A single, fixed time point. Cost-effective but cannot capture the change process.', 6, []),
    ('longitudinal', 'Longitudinal', 'Multiple time points over an extended period (Time series, panel, cohort). Costly, but powerful for analyzing change.', 6, []),
    ('quantitative', 'Quantitative', 'Deductive reasoning, objective reality, numbers, and statistical analysis.', 7, ['quantitative research']),
    ('qualitative', 'Qualitative', 'Inductive reasoning, subjective reality, human behavior, and natural settings.', 7, ['qualitative research']),
    ('mixed', 'Mixed Methods', 'Combining paradigms for superior evidence and comprehensive insight.', 7, []),
    ('survey', 'Survey', 'Uses interviews and questionnaires to judge behavior with intense precision across one or multiple groups.', 8, []),
    ('correlational', 'Correlational', 'Tests relationships between 2+ variables to predict future conditions (Note: Correlation does not equate to causation).', 8, []),
    ('causal-comparative', 'Causal-Comparative', 'Identifies how different groups are affected by the same circumstance without manipulating variables.', 8, []),
    ('naturalistic', 'The Naturalistic Lens', 'Focuses on in-depth, subjective descriptions of human complexity in natural settings, unbound by existing theories.', 10, []),
    ('orientation', 'Orientation & Overview', 'Determining what is salient about the phenomenon.', 10, []),
    ('focused-exploration', 'Focused Exploration', 'In-depth scrutiny based on the outcomes of Phase 1.', 10, []),
    ('confirmation', 'Confirmation & Closure', 'Establishing trustworthiness by verifying findings with participants.', 10, []),
    ('phenomenology', 'Phenomenology', 'Focuses on lived experiences. Assumes each person has their own subjective reality. Contains no rigidly defined steps to preserve creativity.', 11, []),
    ('ethnography', 'Ethnography', 'Focuses on cultural characteristics. Requires the researcher to immerse themselves in the culture and utilize key informants.', 11, []),
    ('case-study', 'Case Study', 'An in-depth observation of a specific person, group, or event over time. Utilizes interviews, field notes, and direct observation.', 11, []),
    ('triangulation', 'Triangulation', 'Corroborating results across different methods', 12, []),
    ('expansion', 'Expansion', 'Broadening the overarching range of inquiry', 12, []),
    ('development', 'Development', 'Using findings from one method to inform the other', 12, []),
    ('complementarity', 'Complementarity', 'Clarifying the results of one method with the other', 12, []),
    ('initiation', 'Initiation', 'Discovering paradoxes to re-frame research questions', 12, []),
    ('mixed-method', 'Mixed Method', 'paradigms split by phase', 12, []),
    ('mixed-model', 'Mixed Model', 'paradigms mixed within a single stage', 12, []),
]:
    add('approaches', key, term, text, [page], 'architecture', aliases=aliases)
add('approaches', 'survey', 'Survey', 'Assess opinions or characteristics that exist at a given time.', [79])
add('approaches', 'qualitative', 'Qualitative', 'Discover potential relationships; descriptive.', [79])
detail(entries['approaches-naturalistic'], 'Limitations as printed on the slide', 'Reductionist by nature\nHighly subjective\nInherently limited to small sample sizes', [10], 'architecture')

# e-Research, infrastructure, comparison and final ecosystem diagram.
for key, term, text in [
    ('e-research', 'e-Research', 'Collaboration, advanced visualization, and global research data management.'),
    ('middleware', 'Middleware', 'Software providing standard community tools and services for seamless knowledge sharing.'),
    ('grid', 'Grid', 'The collection of data repositories, specialized scientific equipment, and pooled computing power.'),
    ('cyberinfrastructure', 'Cyberinfrastructure', 'The overarching computing and network environments that enable virtual e-science communities.'),
]:
    add('digital', key, term, text, [13], 'architecture')
for key, term, traditional, modern in [
    ('participants', 'Participants', 'Individual/local teams', 'Diversely skilled, distributed global teams.'),
    ('data', 'Data', 'Locally generated and stored', 'Globally generated, stored, and accessible.'),
    ('computation', 'Computation', 'Run on researcher’s own local computers', 'Large-scale, on-demand computation and shared instruments.'),
    ('networking', 'Networking', 'Not reliant on the internet', 'Entirely reliant on internet and middleware.'),
    ('dissemination', 'Dissemination', 'Print publications and physical conferences', 'Websites and specialized web portals.'),
]:
    add('digital', key, term, traditional, [14], 'architecture', label='Traditional')
    add('digital', key, term, modern, [14], 'architecture', label='e-Research')
for key, term, text in [
    ('input', 'The Input', 'Purpose & Goals (Exploratory, Descriptive, Explanatory)'),
    ('engine', 'The Engine', 'Methodologies (Quantitative, Qualitative, Mixed) interacting with Time Dimensions (Cross-sectional, Longitudinal)'),
    ('infrastructure', 'The Infrastructure', 'The e-Research Cyberinfrastructure Stack (enabling global scale)'),
    ('output', 'The Output', 'Translating inquiry into evidence-based practice and societal mobilization'),
]:
    add('digital', key, term, text, [15], 'architecture')

# Reliability: differing deck definitions stay separate. Formulas are visually checked.
for key, term, text, overview, page, modern, formula, variables, worked_page in [
    ('test-retest', 'Test-retest method', 'In this method, the same instrument is administered twice to the same group of subjects and the correlation coefficient is determined.', 'Temporal stability across administrations.', 3,
     'The identical assessment instrument is administered twice to the same cohort over a predetermined time interval.\nWhen participant scores are expressed as ordinal rankings, Spearman\'s rank correlation coefficient calculates the consistency of ranking stability.',
     'rₛ = 1 − (6 Σ D²) / (N³ − N)', 'Where D represents rank differences and N is sample size.', 4),
    ('parallel-forms', 'Parallel-forms method', 'Parallel or equivalent forms of a test may be administered of the group of subjects, and the paired observations correlated', 'Equivalence across alternate instruments.', 5,
     'Two equivalent test forms with identical blueprints are administered to the same group to gauge form equivalence.\nPaired observation scores are correlated using the Pearson product-moment correlation formula.',
     'r = [N Σ XY − (Σ X)(Σ Y)] / √([N Σ X² − (Σ X)²][N Σ Y² − (Σ Y)²])', 'Where X is Form A and Y is Form B.', 6),
    ('split-half', 'Split-half method', 'The test in this method may be administered twice, but the test items are divided into two values.', 'Spearman-Brown internal test partitioning.', 7,
     'A single test is split into equal halves (commonly odd vs. even numbered questions) and correlated.\nBecause dividing test length underestimates full test reliability, the Spearman-Brown prophecy formula restores full-scale estimation.',
     'rwt = 2(rht) / (1 + rht)', 'Where rwt is whole-test reliability and rht is half-test correlation.', 8),
    ('internal-consistency', 'Internal-consistency method', 'This method is used with psychological test which consist of dichotomously scored items.', 'Homogeneity across dichotomous items.', 9,
     'KR-20 evaluates item homogeneity across tests containing dichotomously scored items (scored right/wrong or 1/0).\nIt calculates test variance against the sum of individual item variances across all test questions.',
     'Rₓₓ = [N / (N − 1)] [(SD² − Σ pᵢqᵢ) / SD²]', 'Where N = test items, p = pass rate, and q = fail rate (1 − p).', 10),
]:
    e = add('reliability', key, term, text, [28], aliases={'test-retest':['Spearman','Spearman rank correlation'],'parallel-forms':['Pearson','product-moment correlation'],'split-half':['Spearman-Brown','prophecy formula'],'internal-consistency':['KR-20','Kuder-Richardson Formula 20']}.get(key, []))
    add('reliability', key, term, overview, [2], 'reliability', label='Overview')
    add('reliability', key, term, modern, [page], 'reliability')
    detail(e, 'Formula and symbols', variables, [page], 'reliability', formula=formula)
    if key == 'split-half':
        clarify(e, 'reliability-split-conflict')
    # Worked data/steps are transcribed separately, not inferred from the MCQ answer key.
    if key == 'test-retest':
        detail(e, 'Worked example', 'Evaluation (N = 5)\nDenominator: 5³ − 5 = 125 − 5 = 120\nNumerator: 6 × Σ D² = 6 × 2 = 12\nFraction: 12 ÷ 120 = 0.10\nrs = 1 − 0.10 = 0.90\nHigh temporal rank stability.', [4], 'reliability', table={'headers':['Student','Rank 1','Rank 2','D (Diff)','D²'],'rows':[['A',1,1,0,0],['B',2,3,-1,1],['C',3,2,'+1',1],['D',4,4,0,0],['E',5,5,0,0],['Total Σ D²','','','',2]]})
    elif key == 'parallel-forms':
        detail(e, 'Worked example', 'Formula Substitution\nNumerator: 5(228) − (32)(32) = 1140 − 1024 = 116\nDenominator: √[(1170 − 1024)(1130 − 1024)]\nDenominator: √(146 × 106) = √15476 ≈ 124.40\nr = 116 ÷ 124.40 = 0.93\nHigh parallel-form equivalence.', [6], 'reliability', table={'headers':['Student','Form A (X)','Form B (Y)','X²','Y²','XY'],'rows':[[1,10,9,100,81,90],[2,8,8,64,64,64],[3,6,7,36,49,42],[4,5,4,25,16,20],[5,3,4,9,16,12],['Total',32,32,234,226,228]]})
    elif key == 'split-half':
        detail(e, 'Worked example', 'Step 1\nOdd-Even Partition\nCorrelated half-test correlation rht = 0.70.\n\nStep 2\nFormula Substitution\nrwt = 2(0.70) / (1 + 0.70).\n\nStep 3\nFraction Resolution\n1.40 ÷ 1.70 = 0.824.\n\nCalculated Whole-Test Reliability\nSpearman-Brown correction increases reliability from 0.70 to 0.82.\nrwt = 0.82', [8], 'reliability')
    else:
        detail(e, 'Worked example', 'Item Count (N)\n10\nTotal Variance (SD²)\n4.00\nItem Variances (Σ pq)\n1.60\n\n1. Scale Multiplier: [N / (N − 1)] = 10 ÷ 9 = 1.111\n2. Variance Ratio: [(4.00 − 1.60) / 4.00] = 2.40 ÷ 4.00 = 0.600\n3. Product: 1.111 × 0.600 = 0.667\nKR-20 RELIABILITY\n0.67', [10], 'reliability')
for key, term, range_text, application in [
    ('excellent', 'Excellent', 'r ≥ 0.90', 'High-stakes diagnostic decisions.'),
    ('good', 'Good', '0.80 ≤ r < 0.90', 'Classroom grading and certification.'),
    ('acceptable', 'Acceptable', '0.70 ≤ r < 0.80', 'Formative tests and research surveys.'),
    ('questionable', 'Questionable', 'r < 0.70', 'Requires item revision or test lengthening.'),
]:
    add('reliability', key, term, range_text + '\n' + application, [11], 'reliability', aliases=['reliability coefficient benchmarks'])


def write_outputs():
    # The same concept is one entry even when taught in two topic contexts.
    for canonical, duplicate, related in [
        ('literature-primary', 'historical-primary', 'historical'),
        ('literature-secondary', 'historical-secondary', 'historical'),
        ('designs-quasi-experimental', 'experimental-quasi-experimental', 'experimental'),
    ]:
        target, other = entries[canonical], entries.pop(duplicate)
        target['definitions'].extend(other['definitions'])
        target['details'].extend(other['details'])
        target['aliases'].extend(alias for alias in [other['term'], *other['aliases']] if alias not in target['aliases'])
        target['relatedTopics'] = [related]
    result = {'version': 1, 'title': 'Terms', 'entries': list(entries.values())}
    (ROOT / 'data/terms.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    (ROOT / 'data/terms.js').write_text('window.RESEARCH_TERMS = ' + json.dumps(result, ensure_ascii=False, separators=(',', ':')) + ';\n', encoding='utf8')
    inventory = []
    # Each page receives a glossary-specific disposition, not just the old MCQ coverage.
    exceptions = {
        ('methods', 20): 'Researcher qualities are named, not individually defined; retained as one exact list.',
        ('methods', 21): 'Classification chart retained as a list. Unexplained labels receive no invented individual definitions.',
        ('methods', 28): 'Malformed formula glyphs are not reconstructed as quotations; readable formulas come from reliability pages 3/5/7/9.',
        ('methods', 34): 'Characteristics are list labels without definitions; retained together under Research Problem details.',
        ('methods', 36): 'Final guideline ends at “that is,”; incomplete wording retained.',
        ('methods', 74): 'Concept labels only; no independent definitions. Defined variable types are covered on page 23; extraneous/conformed relationships remain undefined here.',
        ('methods', 79): 'Cohort-sequential purpose ends at “overlapping”; its example is clipped. No missing wording supplied.',
        ('methods', 89): 'Overlapped attribution below the second paragraph is not reconstructed.',
        ('methods', 90): 'Lower narrative lines overlap the example panel. Only the complete legible introductory passage is quoted.',
        ('methods', 91): 'Values are supporting benefits, not definitions; two benefit boxes contain clipped/merged wording and are not reconstructed.',
        ('methods', 93): 'Low-contrast case-study text overflows its box; an enlarged crop makes the ending readable, and the full visible description is retained.',
        ('methods', 94): 'Two inconsistent comparative descriptions retained separately, with existing verified clarification.',
        ('methods', 98): '7 Ms are an exact list; no individual meanings invented.',
        ('methods', 99): 'Plan items retained together; History/Maturation/etc. are named but not defined.',
        ('methods', 100): 'Diagram placement is confusing; each displayed notation is explicitly labeled as a source quotation.',
        ('methods', 102): 'Posttest-only description ends at “or”; incomplete wording retained.',
        ('methods', 103): 'Nonequivalent description has a clipped ending; printed extra X retained with clarification. Ambiguous separate-sample schematic is not reconstructed.',
        ('architecture', 9): 'Design categories list examples rather than definitions; source wording and external-validity clarification retained.',
        ('reliability', 4): 'Overlapping worked steps were read visually and laid out in reading order without changing wording.',
        ('reliability', 7): 'Overlapping descriptive lines were read visually; conflicting administration wording in methods p28 remains a separate version.',
        ('reliability', 10): 'Overlapping labels/calculations were read visually and laid out in reading order.',
    }
    administrative = {'methods': set(range(1,17)) | {30,39,40,50,69,80,88,95}, 'architecture': {1}, 'reliability': {1,12}}
    for source in BANK['sources']:
        sid = source['id']
        for page in range(1, source['pages']+1):
            definition_ids, detail_ids = [], []
            for e in result['entries']:
                if any(s['sourceId']==sid and page in s['pages'] for d in e['definitions'] for s in d['sources']):
                    definition_ids.append(e['id'])
                if any(s['sourceId']==sid and page in s['pages'] for d in e['details'] for s in d['sources']):
                    detail_ids.append(e['id'])
            disposition = 'covered' if definition_ids else 'supporting material'
            reason = 'Exact description/list quotation.' if definition_ids else ('Supporting quotation in entry details.' if detail_ids else 'Supporting benefits, summary, or labels without a standalone definition.')
            if page in administrative[sid]:
                disposition = 'excluded'
                reason = 'Title, administrative/course outline, references, section divider, blank worksheet, or closing summary; no glossary definition.'
            if sid == 'methods' and page == 32:
                disposition = 'repeated material'; reason = 'Same research-problem wording as page 31; both citations retained.'
            if sid == 'methods' and page == 49:
                disposition = 'repeated material'; reason = 'Same scope/limitations wording as page 47; both citations retained.'
            inventory.append({'sourceId':sid,'page':page,'disposition':disposition,'reason':reason,'definitionIds':definition_ids,'detailIds':detail_ids,'visualReview':True,**({'exception':exceptions[(sid,page)]} if (sid,page) in exceptions else {})})
    (ROOT / 'audit/terms-inventory.json').write_text(json.dumps({'pages':inventory,'termCount':len(entries),'reviewDate':'2026-11-04'},ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(f'Authored {len(entries)} terms; inventoried {len(inventory)} source pages.')


if __name__ == '__main__':
    write_outputs()
