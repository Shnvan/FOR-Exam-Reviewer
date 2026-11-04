"""Curated slide transcription and question authoring. Originals are read-only.

Run from the project root. No network or OCR is required to rebuild.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = [
    {'id':'methods','filename':'methodsofresearch1.pptx.pdf','pages':104,'label':'Methods of Research'},
    {'id':'architecture','filename':'Modern_Research_Architecture.pptx.pdf','pages':15,'label':'The Architecture of Inquiry'},
    {'id':'reliability','filename':'Methods-of-Estimating-Test-Reliability.pptx.pdf','pages':12,'label':'Estimating Test Reliability'},
]
TOPICS = [
    ('foundations','Research foundations','Purpose, characteristics, qualities, and classifications.'),
    ('variables','Variables & the research process','Identify variables and follow the inquiry process.'),
    ('problems','Problems, titles & objectives','Choose, formulate, and define a research problem.'),
    ('frameworks','Hypotheses & frameworks','Hypotheses, assumptions, significance, scope, and definitions.'),
    ('instruments','Research instruments','Validity, reliability, usability, and scoring.'),
    ('literature','Literature & sources','Reviews, legal bases, local/foreign studies, and source types.'),
    ('designs','Research design essentials','Design components, approaches, controls, and comparisons.'),
    ('historical','Historical research','Evidence, source criticism, uses, and research steps.'),
    ('descriptive','Descriptive research','Survey, normative, correlational, evaluative, and related designs.'),
    ('experimental','Experimental research','Treatment groups, plans, threats, and nine design patterns.'),
    ('approaches','Modern research approaches','Quantitative, qualitative, mixed methods, and time dimensions.'),
    ('digital','e-Research & infrastructure','Cyberinfrastructure, collaboration, and the modern research ecosystem.'),
    ('reliability','Reliability methods & calculations','Spearman, Pearson, Spearman-Brown, KR-20, and interpretation.'),
]
REFS = {
 'sources': {'title':'Library of Congress: primary and secondary sources','url':'https://ask.loc.gov/faq/303148'},
 'framework': {'title':'USC Libraries: theoretical framework','url':'https://libguides.usc.edu/writingguide/theoreticalframework'},
 'split': {'title':'UConn: instrument reliability','url':'https://researchbasics.education.uconn.edu/instrument_reliability/'},
 'spearman-brown': {'title':'ETS: reliability from comparable test halves','url':'https://www.ets.org/research/policy_research_reports/publications/report/1950/ikve.html'},
 'validity': {'title':'BCcampus: experiment basics and validity','url':'https://opentextbc.ca/researchmethods/chapter/experiment-basics/'},
 'quasi': {'title':'KPU: non-equivalent groups designs','url':'https://kpu.pressbooks.pub/psychmethods4e/chapter/non-equivalent-control-group-designs/'},
 'comparison': {'title':'University of Kansas: designs with comparison groups','url':'https://opentext.ku.edu/assessmentevaluationhighered/chapter/chapter-14-designs-involving-comparison-groups/'},
}
QUESTIONS=[]

def add(topic, key, prompt, answer, wrong, pages, explanation=None, source='methods', note=None, refs=(), extra=(), kind='concept', **kwargs):
    assert len(wrong)==3 and len(set([answer]+wrong))==4, (key,answer,wrong)
    qid=f'{topic}-{key}'
    # Balanced, deterministic answer locations, with stable semantic choice IDs.
    correct={'id':'answer','text':answer}
    choices=[{'id':f'd{i+1}','text':w} for i,w in enumerate(wrong)]
    choices.insert(int(hashlib.sha256(qid.encode()).hexdigest()[:8],16)%4,correct)
    q={'id':qid,'topic':topic,'prompt':prompt,'choices':choices,'correctChoiceId':'answer',
       'explanation':explanation or f'{answer}: {prompt.rstrip("?")}.',
       'sources':[{'sourceId':source,'pages':pages}]+list(extra),'kind':kind}
    if note:
        assert refs, f'Clarification needs a verified reference: {qid}'
        q['clarification']={'text':note,'references':[REFS[r] for r in refs]}
        q['scoringBasis']='slide-stated'
        # All affected questions visibly identify their source and page.
        if 'according to' not in prompt.lower():
            label=next(s['label'] for s in SOURCES if s['id']==source)
            q['prompt']=f'According to {label}, PDF page {pages[0]}, {prompt[0].lower()+prompt[1:]}'
    q.update(kwargs)
    QUESTIONS.append(q)
    return q

def identify(topic, rows, pages, source='methods', prefix='Which term', extra=()):
    """Rows are manually authored term-definition pairs; alternatives are peers."""
    for i,(key,term,definition) in enumerate(rows):
        peers=[r[1] for r in rows if r[1]!=term]
        assert len(peers)>=3
        wrong=[peers[(i+j)%len(peers)] for j in range(3)]
        add(topic,key,f'{prefix} matches this description: {definition}?',term,wrong,pages,
            f'The slide associates {term} with: {definition}.',source=source,extra=extra)

# METHODS OF RESEARCH: foundations and slide lists.
add('foundations','definition','What is the central description of research in the summary on PDF page 17?',
    'An organized and systematic way of finding answers to questions',
    ['Collecting opinions without a planned method','Accepting an explanation without checking evidence','Repeating information without investigating a question'],[17],
    'The slide summarizes the author definitions as organized, systematic inquiry directed at answering questions.')
add('foundations','good-definition','Which author definition emphasizes careful, critical, disciplined inquiry directed toward resolving a problem?',
    'Good (1972)',['Manuel and Medel (1976)','Sanchez (1980)','Treece and Treece (1973)'],[17],
    'Good emphasizes critical, disciplined inquiry; Manuel and Medel emphasize gathering information scientifically; Sanchez emphasizes systematic investigation; Treece and Treece emphasize controlled data and prediction/explanation.')
add('foundations','manuel-definition','Which definition on page 17 emphasizes gathering information to solve a particular problem in a scientific manner?',
    'Manuel and Medel (1976)',['Good (1972)','Sanchez (1980)','Treece and Treece (1973)'],[17],
    'The Manuel and Medel definition appears twice on the slide; it is represented once in this bank.')
add('foundations','sanchez-definition','Who describes research as systematic investigation to answer questions posed by the researcher?',
    'Sanchez (1980)',['Good (1972)','Manuel and Medel (1976)','Treece and Treece (1973)'],[17],
    'Sanchez emphasizes systematic investigation and researcher-posed questions.')
add('foundations','treece-definition','Which definition connects rigorously controlled data collection with prediction or explanation?',
    'Treece and Treece (1973)',['Good (1972)','Manuel and Medel (1976)','Sanchez (1980)'],[17],
    'Treece and Treece connect solving problems with controlled data collection and prediction/explanation.')
importance=[
 ('service','Serving people','To serve people and provide a good life'),
 ('unknown','Discovering the unknown','To find more facts about unknown phenomena'),
 ('existing','Using existing information','To answer problems using existing methods and information'),
 ('innovation','Improving techniques and products','To improve existing techniques and develop new instruments or products'),
 ('substance','Discovering unrecognized substances','To find a previously unrecognized substance'),
 ('action','Discovering pathways of action','To discover possible courses of action'),
 ('science','Systematizing science','To organize related valid generalizations into systematized science'),
 ('decisions','Supporting decisions','To provide a basis for decision making'),
 ('curiosity','Satisfying curiosity','To satisfy the researcher\'s curiosity'),
 ('queries','Answering queries','To find answers to queries'),
 ('understanding','Deepening understanding','To acquire better and deeper understanding'),
 ('knowledge','Expanding and verifying knowledge','To expand and verify existing knowledge'),
 ('efficiency','Improving efficiency and quality','To improve efficiency, efficacy, and quality'),
 ('exports','Improving exportation of goods','To improve exportation of goods'),
 ('economy','Responding to economic needs','To respond to economic recovery and austerity'),
]
identify('foundations',importance,[18],prefix='Which importance of research on the slide')
identify('foundations',[
 ('empirical','Empirical','Uses direct experience or observation'),
 ('logical','Logical','Follows valid procedures and principles'),
 ('cyclical','Cyclical','Starts with a problem and ends with a problem'),
 ('analytical','Analytical','Uses proven analytical procedures'),
 ('critical','Critical','Exhibits careful and precise judgment'),
 ('methodical','Methodical','Uses systematic methods and procedures'),
 ('replicable','Replicability','Can be repeated to reach valid, conclusive results'),
],[19],prefix='Which characteristic of research')
researcher=[('oriented','Research oriented','Keeps inquiry and investigation central'),('efficient','Efficient','Uses resources with minimal waste'),
 ('scientific','Scientific','Uses scientific inquiry rather than unsupported belief'),('effective','Effective','Achieves the intended research outcome'),
 ('active','Active','Participates actively in research work'),('resourceful','Resourceful','Finds useful sources and ways to overcome resource problems'),
 ('creative','Creative','Develops original approaches and ideas'),('honest','Honest','Reports evidence truthfully'),
 ('economical','Economical','Uses research funds prudently'),('religious','Religious','Completes the final R in the slide\'s RESEARCHER mnemonic')]
identify('foundations',researcher,[20],prefix='Which quality in the slide\'s RESEARCHER mnemonic')
add('foundations','researcher-outcome','What outcome does page 20 associate with possessing the listed researcher qualities?',
 'Completing projects promptly and responding to socioeconomic recovery',
 ['Eliminating the need for research methods','Guaranteeing every hypothesis is confirmed','Avoiding all use of money and equipment'],[20],
 'The slide links the mnemonic qualities to shorter project completion and socioeconomic recovery; this is the slide\'s stated aspiration, not a guaranteed outcome.')
classification=[
 ('purpose','Purpose','Predictive, directive, and illuminative research'),
 ('goal','Goal','Basic or pure research and applied research'),
 ('level','Levels of investigation','Exploratory, descriptive, and experimental research'),
 ('analysis','Type of analysis','Analytic and holistic research'),
 ('scope','Scope','Action research'),
 ('choice','Choice of answer','Evaluation and developmental research'),
 ('statistics','Statistical content','Quantitative and non-quantitative research'),
 ('time','Time element','Historical, descriptive, and experimental research'),
]
identify('foundations',classification,[21],prefix='According to the classification diagram on PDF page 21, which classification axis')

# VARIABLES and two process diagrams.
add('variables','definition','What is a variable?', 'A quantity or characteristic that can take different values',
 ['A feature that must have one fixed value in all observations','A bibliography entry','A guaranteed conclusion'],[22],
 'The slide describes variables as quantities susceptible to change or characteristics with different values/properties.')
identify('variables',[
 ('independent','Independent variable','Is the stimulus selected by the researcher to examine its relationship to an observed phenomenon'),
 ('dependent','Dependent variable','Is the observed or measured response to the independent variable'),
 ('intervening','Intervening variable','Intrudes between the independent and dependent variables and affects their relationship'),
 ('control','Control variable','Is controlled so its effects can be neutralized or removed'),
 ('moderator','Moderator variable','Is selected to determine whether it alters the relationship between independent and dependent variables'),
],[23],extra=({'sourceId':'methods','pages':[74]},))
for key,prompt,ans,wrong in [
 ('study-hours','In the page 24 example, which variable is shown as the input related to mathematics scores?','Number of hours studying',['Mathematics scores','Fish weight increment','Salinity']),
 ('study-output','In the page 24 example, what is the outcome associated with hours studying mathematics?','Mathematics scores',['Number of hours studying','Bread meal','Water temperature']),
 ('study-middle','Which set appears BETWEEN study hours and mathematics scores in the diagram?','Age, gender, socioeconomic factors, and attitudes toward study',['Fish cages, pellets, and bread meal','Score, grade, and mathematics test results','Literature, bibliography, and thesis title']),
 ('fish-input','In the grouper example, which factor is the input?','Pellets and bread meal as supplemental feeds',['Weight increment','Researcher age','Mathematics scores']),
 ('fish-output','In the grouper example, which variable is measured as the outcome?','Weight increment',['Pellets and bread meal','Fish-cage design title','Students\' study hours']),
 ('fish-middle','Which environmental factors appear between supplemental feed and weight increment?','Salinity, oxygen, temperature, and pH',['Age, gender, and attitudes','Research title and significance','Sample rank and test variance']),
]: add('variables',key,prompt,ans,wrong,[24],f'The page 24 diagram links the input through the listed intervening/environmental factors to the outcome: {ans}.',kind='application')
process=['Problem / objectives','Theoretical / conceptual framework','Assumptions','Hypothesis','Review of related literature','Research design','Data collection','Data processing','Statistical treatment','Analysis and interpretation','Summary, conclusion, and recommendation']
for i,step in enumerate(process):
 wrong=[process[(i+d)%len(process)] for d in [2,4,6]]
 add('variables',f'process-{i+1}',f'In the numbered research-process diagram on PDF page 25, what is step {i+1}?',step,wrong,[25],f'Step {i+1} is {step}. '+('It follows '+process[i-1]+'.' if i else 'The process begins by identifying the problem and objectives.'))
for key,prompt,ans,wrong in [
 ('flow-start','What begins the detailed research-process flowchart on PDF page 26?','Identification and definition of a research problem',['Report preparation and dissemination','Data encoding','Statistical analysis']),
 ('flow-hypothesis','Which step brings together the problem/objectives, framework, and operational definitions in the detailed flowchart?','Hypothesis formulation',['Data-file creation','Information dissemination','Quality control']),
 ('flow-design','What follows hypothesis formulation in that flowchart?','Choosing an appropriate research design',['Writing recommendations immediately','Tabulating final results','Preparing a bibliography only']),
 ('flow-population','What comes between choosing the design and collecting data in the detailed flowchart?','Identification of target population and sampling',['Final report publication','Hypothesis rejection','Conclusion writing']),
 ('flow-instrument','Which data-collection preparation step develops the measurement tool?','Preparation of the research instrument',['Data dissemination','Creation of conclusions','Review of export figures']),
 ('flow-validation','Which step checks the instrument before its use?','Reliability testing and validation',['Skipping the pilot stage','Interpreting conclusions','Publishing unprocessed data']),
 ('flow-methods','Which methods are named under data collection in the detailed flowchart?','Questionnaire administration, interviewing, testing, and observation',['Only library cataloging','Only tabulation and coding','Only conclusion and recommendation writing']),
 ('flow-quality','What checks the quality of the data-collection work in the detailed diagram?','Quality control',['Title capitalization','Export promotion','Publication pricing']),
 ('flow-processing','Which activities belong to data processing in the flowchart?','Editing, coding, encoding, data-file creation, and tabulation',['Hypothesis formulation and source criticism only','Recruitment and experimental treatment only','Publication and policy implementation only']),
 ('flow-analysis','Which activities belong to data analysis and interpretation in the flowchart?','Statistical analysis, interpretation, and generalization',['Writing the research title only','Printing instruments only','Random assignment only']),
 ('flow-final','What is the final box of the detailed research-process flowchart?','Report preparation and information dissemination',['Identification of target population','Preparation of the instrument','Hypothesis formulation']),
]: add('variables',key,prompt,ans,wrong,[26],f'The detailed process diagram explicitly places {ans.lower()} in this part of the workflow.')

# PROBLEM selection, formulation, title rules.
add('problems','definition','What makes a situation a research problem in the supplied definition?',
 'It is a significant, perplexing situation whose solution requires reflective inquiry',
 ['It has already been answered completely and needs no evidence','It is any personal preference without a question','It is only a statement of the final findings'],[31,32],
 'A research problem is significant and challenging; it is translated into questions that guide inquiry.')
identify('problems',[
 ('why','Why','Asks the aim or purpose of the investigation'),('what','What','Asks the subject matter or topic investigated'),
 ('where','Where','Asks the place or locale of the research'),('when','When','Asks the period during which data are gathered'),
 ('who','Who','Asks the population from whom data are collected'),
],[33],prefix='Which element of a research problem')
identify('problems',[
 ('novelty','Novelty','Adds a new angle rather than merely repeating what is already known'),
 ('interesting','Interesting','Engages the researcher\'s interest'),('relevant','Relevant','Relates meaningfully to the issue or field'),
 ('feasible','Feasible','Can be undertaken with available resources and constraints'),
 ('researchable','Researchable (SMART)','Can be investigated through a clear researchable problem'),
 ('ethical','Ethical','Respects ethical considerations'),('systematic','Systematic','Follows an orderly approach'),
],[34],prefix='Which characteristic of a good research problem')
identify('problems',[
 ('source-specialization','Researcher specialization','Derives a problem from the investigator\'s own field'),
 ('source-past','Current and past research','Finds a problem in existing investigations'),
 ('source-recommendations','Thesis and journal recommendations','Uses recommendations left by earlier researchers'),
 ('source-local','Original ideas from local problems','Develops a creative problem based on issues encountered in the locality'),
],[35],prefix='Which source of research problems')
guidelines=[
 ('self','The researcher should choose the problem','Who should select the research problem according to page 36?',['The researcher should accept any randomly assigned trend','Only a publisher should choose it','It should be chosen after data analysis']),
 ('interest','It should be within the researcher\'s interest','Which selection guideline concerns motivation?',['It should be unrelated to the researcher\'s interest','Interest should replace all evidence','It should depend only on popularity']),
 ('specialization','It should fit the researcher\'s specialization','Which selection guideline concerns the researcher\'s field?',['It must be outside all known disciplines','It should avoid the researcher\'s field','Only the title length matters']),
 ('competence','It should be within the researcher\'s competence','Which guideline concerns the ability to tackle the problem?',['It must require skills that cannot be obtained','Competence matters only after publication','A difficult title guarantees competence']),
 ('finance','The researcher must be able to finance it or find funding','Which guideline concerns the project budget?',['Funding should never be considered','Only expensive studies are researchable','Costs are determined after publication']),
 ('manage','It should be researchable and manageable','Which guideline addresses whether the project can realistically be completed?',['It must have unlimited scope','It should require unavailable resources','It must avoid any measurable question']),
]
for key,ans,prompt,wrong in guidelines:add('problems','selection-'+key,prompt,ans,wrong,[36],ans+'.')
formulation=[
 ('before','Before conducting the research','When should general and specific research problems be formulated?',['Only after conclusions are written','Only after publication','Only after final statistical analysis']),
 ('interrogative','In interrogative form','How are specific subproblems customarily stated?',['As final conclusions','As unrelated keywords','As a bibliography']),
 ('clear','Clear and unequivocal','How should each specific question be worded?',['Ambiguous and open to several meanings','As long as possible without a focus','Without stating any research concern']),
 ('independent','Separately researchable from the other questions','What does page 37 require of each specific question?',['Its answer must already appear in every other question','It must duplicate all other questions','It must be unrelated to the general problem']),
 ('known','Known facts and phenomena','What should each specific question be based on?',['Invented results','An unsupported final conclusion','The cost of printing alone']),
 ('separate-answers','Answers should be interpretable separately','How should answers to individual specific questions relate?',['Every answer must be identical','No answer may be interpreted on its own','All questions must share one prewritten result']),
 ('contribute','They should contribute to the whole research problem','What should the answers to specific questions accomplish?',['Replace the need for a general problem','Avoid the study\'s topic','Guarantee a preferred result']),
 ('sufficient','Enough questions to cover development of the whole problem','How many specific questions should be formulated?',['Exactly two regardless of the study','As many as possible without relevance','Only questions answerable without data']),
 ('combined','Their combined answers should develop the entire study','What should summing the specific-question answers provide?',['A substitute for all source evidence','Unrelated findings only','A guarantee of statistical significance']),
 ('general','A general problem broken into specific questions','What overall structure is recommended for the problem statement?',['Only isolated questions with no general focus','A conclusion followed by unrelated titles','Only a list of books']),
]
for key,ans,prompt,wrong in formulation:add('problems','formulation-'+key,prompt,ans,wrong,[37],f'The formulation guidance calls for {ans[0].lower()+ans[1:]}.')
for key,prompt,ans,wrong in [
 ('attention','What should a research title do to the reader?','Grab attention and encourage further reading',['Disclose fabricated findings','Avoid any clue to the topic','Replace the research problem']),
 ('thought','What intellectual quality should the title have?','Be intriguing and thought-provoking',['Be deliberately misleading','Use unexplained abbreviations only','Avoid a clear topic']),
 ('five-w','Which elements should a title include according to the slide?','The 5Ws',['Only the researcher\'s name','Only the bibliography year','The answer key']),
 ('length','According to the title-writing slide on PDF page 38, what maximum length is recommended?','20 words',['5 words','50 words','100 words']),
 ('format','According to page 38, what presentation is recommended for the title?','Inverted-pyramid layout and capital letters',['A circular paragraph in lowercase','A table of statistics only','A bibliography entry in italics only']),
 ('avoid','Which opening phrases does page 38 recommend avoiding?','A study of, an investigation of, an analysis of',['Specific population and locale','Relevant variables and time period','Clear topic words']),
 ('institution','Which requirement takes account of the school\'s prescribed title format?','Follow the format required by the institution',['Ignore all institutional requirements','Use one universal style in every institution','Use only the researcher\'s preferred style']),
]:add('problems','title-'+key,prompt,ans,wrong,[38],f'The course title-writing tips state: {ans}. These are slide-specific writing recommendations.')
add('problems','objectives-form','How do research problems and research objectives differ in form?',
 'Problems are interrogative; objectives are declarative',
 ['Problems are declarative; objectives are interrogative','Both must be numerical equations','Objectives are always questions without verbs'],[41],
 'They share characteristics but differ in wording: a problem asks a question, while an objective states an intended aim.')

# HYPOTHESES, frameworks and boundary definitions.
identify('frameworks',[
 ('hypothesis','Hypothesis','Is a provisional or wise guess temporarily adopted to explain observed facts'),
 ('null','Null hypothesis','Denies the existence of the trait, relationship, or difference being tested'),
 ('alternative','Alternative hypothesis','Affirms the existence of the observed phenomenon, relationship, or difference'),
 ('assumption','Assumption','Is presumed true in relation to the research problem'),
],[42,45],prefix='Which research term')
add('frameworks','theoretical','What function is assigned to the theoretical framework on PDF page 43?',
 'Justifying the problem/objectives and providing a legal basis for defining parameters',
 ['Listing only raw questionnaire scores','Replacing the significance of the study with a budget','Presenting only the final recommendations'],[43],
 'This preserves page 43\'s wording about a legal basis.',note='A theoretical framework normally grounds the study in relevant theory and its assumptions. A legal basis is a separate justification, not a defining requirement of a theoretical framework.',refs=('framework',))
add('frameworks','conceptual-framework','What does the conceptual framework present according to the slides?',
 'Specific, well-defined concepts called constructs',['Only the bibliography','Only the financial statement','Only the raw responses'],[44],
 'Page 44 describes a conceptual framework in terms of well-defined concepts or constructs.')
add('frameworks','significance','What is the purpose of the significance-of-the-study section?',
 'Explain the importance of the study convincingly',['List unrelated studies without discussion','State all data as final conclusions','Replace the research instrument'],[46],
 'The slide says significance should be presented comprehensively to convince the screening committee of the study\'s importance.')
add('frameworks','scope','What belongs in the scope and limitations of a study?',
 'Coverage, subjects, instruments, issues, duration, and constraints affecting results',
 ['Only publication references','Only the hypothesis answer','Only a list of definitions'],[47,49],
 'Both pages give the same coverage definition; the repeated slide is represented by the same question.')
for key,prompt,ans,wrong in [
 ('scope-subjects','Which scope element specifies who is studied?','Subjects',['Bibliography style','Cover-letter color','Journal subscription']),
 ('scope-tools','Which scope element identifies the apparatus or equipment used?','Research instruments and equipment',['Publication month only','Author surname only','General dictionary meaning only']),
 ('scope-time','Which scope element identifies how long the research lasts?','Duration of the study',['Alternative hypothesis','Conceptual definition','Legal citation style']),
 ('scope-constraints','Which scope element addresses restrictions with a direct bearing on findings?','Constraints or limitations',['Source typography','Bibliography indentation','Researcher initials']),
]:add('frameworks',key,prompt,ans,wrong,[47,49],f'{ans} is explicitly included in the scope-and-limitations description.')
add('frameworks','conceptual-definition','Which definition gives a term\'s academic, dictionary, or universal meaning?',
 'Conceptual (constitutive) definition',['Operational (functional) definition','Research hypothesis','Experimental treatment'],[48,67],
 'Conceptual definitions are abstract/formal meanings, commonly derived from dictionaries and published works.')
add('frameworks','operational-definition','Which definition explains a term through observable characteristics and how it is used in the study?',
 'Operational (functional) definition',['Conceptual (constitutive) definition','Bibliographic definition','Alternative hypothesis'],[48,68],
 'Operational definitions specify study-specific use or measurement, rather than only a general dictionary meaning.')
add('frameworks','measured-operational','What does a measured operational definition specify?',
 'How a concept is measured in the investigation',['Only its dictionary origin','Only the author\'s academic degree','Only the study title'],[68],
 'Measured operational definitions describe the procedure or measure used for the concept.')
add('frameworks','experimental-operational','What does an experimental operational definition specify?',
 'Details of how a variable is manipulated',['Only its universal dictionary meaning','Only the final result','Only the sampling cost'],[68],
 'The slide contrasts measurement procedures with the details of experimental manipulation.')
add('frameworks','operational-scenario','A study defines achievement as the score on its 40-item test. Which type of definition is this?',
 'Measured operational definition',['Conceptual definition','Null hypothesis','Literature citation'],[48,68],
 'A score on a specified test tells how the concept is measured in this investigation.',kind='application')

# INSTRUMENT quality and usability.
identify('instruments',[
 ('validity','Validity','Measures what the instrument intends to measure'),
 ('reliability','Reliability','Is dependable, consistent, and stable'),
 ('usability','Usability','Can be used satisfactorily without excessive expenditure of time, money, and effort'),
 ('content','Content validity','Has test content representative of the course content'),
 ('concurrent','Concurrent validity','Agrees or correlates with an acceptable criterion measured in the present'),
 ('predictive','Predictive validity','Makes predictions confirmed by later evidence'),
 ('construct','Construct validity','Measures a theoretical construct or trait'),
],[27,28,29])
add('instruments','validity-scenario','A teacher checks whether an exam samples the topics actually taught. Which validity is being examined?',
 'Content validity',['Concurrent validity','Predictive validity','Split-half reliability'],[27],
 'Content validity concerns representation of course topics, not agreement with another measure or future outcomes.',kind='application')
add('instruments','concurrent-scenario','A new instrument is compared with an accepted criterion collected at the same time. What is being examined?',
 'Concurrent validity',['Predictive validity','Usability','Test-retest stability'],[27],
 'The criterion agreement is concurrent; prediction would be confirmed by evidence collected later.',kind='application')
identify('instruments',[
 ('administration','Ease of administration','Requires complete and precise directions for administering the instrument'),
 ('scoring','Ease of scoring','Depends on objective items, prepared answer keys, and understood scoring directions'),
 ('interpretation','Ease of interpretation and application','Uses tables or guidance that make results easy to interpret and apply'),
 ('cost','Low cost','Uses materials practical in cost'),
 ('makeup','Proper mechanical make-up','Is clearly printed in a size appropriate to the learners\' grade or year'),
],[29],prefix='Which usability factor')
for key,ans,wrong,prompt in [
 ('objective','Constructing objective-type items',['Removing all scoring directions','Using an unrelated answer key','Changing the expected answer for each learner'],'Which item-construction practice supports ease of scoring?'),
 ('keys','Adequately preparing answer keys',['Scoring without a criterion','Choosing the most common response as correct','Avoiding written scoring guidance'],'What preparation of grading documents supports ease of scoring?'),
 ('directions','Ensuring scoring directions are understood',['Keeping the marking procedure secret from scorers','Allowing arbitrary grading rules','Using no prepared keys'],'What should scorers understand to facilitate ease of scoring?'),
]:add('instruments','scoring-'+key,prompt,ans,wrong,[29],f'Page 29 lists {ans.lower()} as an aspect of ease of scoring.')

# LITERATURE: every function, characteristic and source category.
add('literature','definition','What is related literature?',
 'Discussions of facts and principles connected to the present study',
 ['Only the investigator\'s unrecorded opinions','A substitute for every research question','Only the final statistical results'],[51,63],
 'Related literature provides documented facts, principles, laws, theories, and observations relevant to the investigation.')
functions=[
 ('select','Selecting a better research problem','Helps choose a better research topic'),
 ('understand','Understanding the research topic','Helps the investigator understand the topic better'),
 ('duplication','Checking duplication','Helps establish what earlier studies have already investigated'),
 ('locate','Locating additional sources','Guides the researcher toward more related information'),
 ('questions','Formulating specific questions','Guides the questions to be researched'),
 ('hypotheses','Formulating assumptions and hypotheses','Guides provisional assumptions and hypotheses'),
 ('framework','Formulating a conceptual framework','Guides the study\'s conceptual structure'),
 ('methods','Selecting research methods','Guides which research approach to apply'),
 ('sampling','Selecting a sampling technique','Guides how the sample is chosen'),
 ('instrument','Preparing and validating instruments','Guides selection, preparation, and validation of data-collection tools'),
 ('statistics','Selecting statistical procedures','Guides which statistical procedures to apply'),
 ('analysis','Analyzing and interpreting data','Guides analysis, organization, presentation, and interpretation'),
 ('conclusions','Developing findings and recommendations','Guides summary, conclusions, and recommendations'),
 ('compare','Comparing findings with earlier research','Helps develop generalizations or principles from comparisons'),
]
for i,row in enumerate(functions):
 key,ans,definition=row
 peers=[r[1] for r in functions if r[1]!=ans]
 add('literature','function-'+key,f'Which function of a literature review {definition[0].lower()+definition[1:]}?',ans,[peers[(i+j)%len(peers)] for j in range(3)],[52] if i<3 else [53] if i<10 else [54],definition+'.')
for key,prompt,ans,wrong in [
 ('recent','How recent should surveyed materials generally be?','As recent as possible',['Always at least 50 years old','Only from the same calendar month','Date never matters']),
 ('permanent','When may an older treatise remain useful?','When it addresses universals or relatively permanent matters',['Only when its author is unknown','Only when it contradicts all current evidence','Only when no relevance is explained']),
 ('past-comparison','When else can older materials be appropriate?','When comparing present conditions with a remote past',['Whenever recent evidence is inconvenient','Only when there are no sources','When the study avoids time comparisons']),
 ('objective','What attitude should the reviewed materials display?','Objectivity and lack of bias',['Unexamined prejudice','A predetermined desired result','Dependence on rumor']),
 ('relevant','How should materials relate to the investigation?','They must be relevant to the study',['They must be unrelated but lengthy','They need only share the author\'s surname','They must avoid the research topic']),
 ('facts','What should the materials be based on?','Original, true facts or data',['Invented evidence','Unidentified gossip','Only the investigator\'s preferred conclusion']),
 ('amount','What does the slide say about the amount of reviewed material?','Neither too few nor too many',['Exactly one source in every study','Unlimited unrelated references','No sources before publication']),
]:add('literature','quality-'+key,prompt,ans,wrong,[55] if key in ['recent','permanent','past-comparison'] else [56],f'The slide\'s review guidance is: {ans}.')
add('literature','source-locations','Which set lists sources of related information named on page 57?',
 'Scholarly journals, books, authoritative databases, and primary sources',
 ['Only anonymous comments and advertisements','Only the researcher\'s draft conclusions','Only the study\'s answer sheet'],[57],
 'The slide also mentions newspapers, magazines, films, and audio/video recordings as possible materials.')
add('literature','primary','What makes a source primary?',
 'It provides original, firsthand evidence about what is being studied',
 ['It must be printed rather than online','It must summarize many other sources','It must be an encyclopedia'],[58,84,85],
 'The definition in the deck emphasizes origin and firsthand participation, not the medium.')
add('literature','secondary','What makes a source secondary?',
 'It discusses or interprets information originally presented elsewhere',
 ['It is always unpublished original research','It is always an eyewitness\'s diary','It must have been written before the event'],[59,84,85],
 'Secondary sources are removed from the original observation and interpret or discuss other evidence.')
add('literature','primary-examples-slide','Which examples are grouped as primary sources on Methods of Research, PDF page 58?',
 'Published books, magazines, encyclopedias, and almanacs',
 ['Only unpublished theses and dissertations','Only data-collection forms','Only interview recordings'],[58],
 'This is the page 58 example list, scored as the slide states.',
 note='Source status depends on the evidence and research question, not publication format. Encyclopedias commonly synthesize earlier evidence. The same deck gives more useful firsthand/secondhand examples on pages 84-85.',refs=('sources',))
add('literature','secondary-examples-slide','Which examples are grouped as secondary sources on Methods of Research, PDF page 59?',
 'Internet information and unpublished theses/dissertations',
 ['Only original eyewitness diaries','Only firsthand photographs','Only original laboratory observations'],[59],
 'This is the example grouping printed on page 59.',
 note='Being online or unpublished does not determine whether a source is primary or secondary. An original thesis can report primary research; online collections can preserve firsthand records. Classify by the role of the evidence.',refs=('sources',))
for key,prompt,ans,wrong in [
 ('libraries','Where may related literature be located?','Government, school, and private libraries',['Only a test-scoring office','Only the study\'s conclusion section','Only a single private notebook']),
 ('offices','Which non-library locations are named for related materials?','Government and private offices',['Only sports facilities','Only retail checkout counters','Only examination seating charts']),
 ('national','Which national institution is named as a rich repository?','The National Library',['The study\'s scoring committee','A private answer-key vendor','The research participant list']),
 ('education','Which department library is named in the historical wording of page 60?','Department of Education, Culture and Sports library',['Department of Trade bibliography unit','Department of Agriculture test room','Department of Finance sampling office']),
]:add('literature','locate-'+key,prompt,ans,wrong,[60],f'Page 60 lists {ans}. The department name is preserved as historical course wording, not a claim about its current name.')
add('literature','legal','What are related legal bases?',
 'Relevant laws and department directives such as orders, circulars, and memoranda',
 ['Only dictionary entries','Only participant preferences','Only statistical frequency tables'],[61,62],
 'Legal bases show how the study relates to government thrusts. Page 62 supplies a historical nursing-law example; it is an example of a legal basis, not current legal advice.')
add('literature','literature-relevance','What must accompany the presentation of related literature?',
 'An explanation of its relevance to the present study',
 ['Only a list of author surnames','Only the publication price','A guarantee that all sources agree'],[63,64],
 'Page 63 rejects presenting literature without explaining its relevance; page 64 illustrates connecting a nursing leadership article to a proposed study.')
add('literature','chronology','According to page 63, how is related literature presented chronologically?',
 'From recent to past',['From longest to shortest','By price from highest to lowest','By author age'],[63],
 'The slide specifies recent-to-past order. This is course-specific presentation guidance rather than a universal requirement for every literature review.')
add('literature','studies','What belongs under related studies?',
 'Relevant published and unpublished research, grouped into local and foreign studies',
 ['Only dictionaries without research findings','Only the current study\'s raw data','Only the researcher\'s personal plans'],[65,66],
 'Page 66 illustrates a local Philippine study about staff-nurse stress, whereas page 64 illustrates a literature article. The relevance to the proposed study must be explained.')
add('literature','local-example','Which example is presented as a LOCAL study?',
 'Sultan\'s 1999 study of stress among nurses at a Quezon City hospital',
 ['A dictionary definition of stress','A general list of legal circulars','An unpublished hypothesis for the current study'],[66],
 'The slide identifies the Quezon City nursing thesis as its local-study example.')

# DESIGN essentials and tabular comparisons.
add('designs','definition','What is a research design?',
 'The blueprint or plan guiding data collection, measurement, and analysis',
 ['Only the color and layout of a report','Only a list of author references','Only the final statistical answer'],[70,71],
 'The design arranges conditions for collection and analysis while relating the purpose of research to practical procedures.')
add('designs','decisions','Which decisions are included in planning a research design?',
 'What, where, when, how much, and by what means the inquiry is conducted',
 ['Only the binding color of the final paper','Only the date of publication','Only the title capitalization'],[70],
 'Page 70 defines the design through the principal decisions needed to conduct an inquiry.')
identify('designs',[
 ('sampling','Sampling design','Chooses the items or participants to be observed'),
 ('observational','Observational design','Specifies the conditions under which observations are made'),
 ('statistical','Statistical design','Decides how the information and data gathered will be analyzed'),
 ('operational','Operational design','Specifies the procedures by which the planned sampling requirements are carried out'),
],[72],prefix='Which part of a research design')
for key,prompt,ans,wrong in [
 ('information','Which design consideration concerns access to evidence?','The means of obtaining information',['Only cover design','Only the researcher\'s initials','Only the page count']),
 ('staff','Which design consideration concerns personnel?','Availability and skills of the researcher and staff',['Only the title font','Only the bibliography order','Only the printing date']),
 ('objective','Which design consideration concerns the intended aim?','The objective of the problem to be studied',['Only the researcher\'s surname','Only the file extension','Only the instrument color']),
 ('nature','Which design consideration concerns what sort of problem is being examined?','The nature of the problem',['Only the publisher location','Only the respondent initials','Only the cover-page margin']),
 ('resources','Which design consideration concerns feasibility of the work?','Availability of time and money',['Only the length of the abstract','Only the journal logo','Only the chapter numbering']),
]:add('designs','feature-'+key,prompt,ans,wrong,[73],f'The features-of-good-design slide names {ans.lower()} as a planning consideration.')
add('designs','confounded','Which important design concept on page 74 concerns relationships entangled with other influences?',
 'Confounded relationships',['Source pagination','Bibliographic indexing','Mechanical make-up'],[74],
 'The slide lists dependent/independent, extraneous, control variables, and confounded relationships as important concepts.')
add('designs','hypothesis','What relationship does a research hypothesis predict according to page 75?',
 'A relationship between an independent and a dependent variable',
 ['Only the relation between two bibliography entries','Only the relation between title and cover color','Only the relation between author and publisher'],[75],
 'The slide describes a research hypothesis as a predictive statement relating independent and dependent variables.')
add('designs','testing','Can hypothesis-testing research be experimental or non-experimental according to page 75?',
 'Yes, the slide explicitly allows both', ['No, it must always be a randomized experiment','No, it must always be historical','No, it excludes any data collection'],[75],
 'Page 75 allows experimental and non-experimental hypothesis testing. This is more qualified than the shorthand on page 76.')
identify('designs',[
 ('exploratory','Exploratory / formulative research','Formulates the research problem and explores an initially unclear area'),
 ('descriptive','Descriptive research','Describes characteristics of an individual or group'),
 ('diagnostic','Diagnostic research','Determines how frequently something occurs'),
 ('hypothesis-testing','Hypothesis-testing studies','Tests a hypothesis about a causal relationship between variables in the page 76 classification'),
],[76],prefix='According to the page 76 classification, which design category')
for key,ans,wrong,prompt in [
 ('literature','Survey of concerning literature',['Publication of final findings','Instrument destruction','Posttest-only scoring'],'Which exploratory approach examines existing publications about the problem?'),
 ('experience','Experience survey',['Random treatment assignment','KR-20 item scoring','A completed conclusion chapter'],'Which exploratory approach draws on experience relevant to the problem?'),
 ('cases','Analysis of insight-stimulating examples',['Discarding all earlier research','Automatic acceptance of assumptions','Omitting the research problem'],'Which exploratory approach examines cases that stimulate insight?'),
]:add('designs','explore-'+key,prompt,ans,wrong,[76],f'Page 76 lists {ans.lower()} as an exploratory approach.')
for key,prompt,ans,wrong in [
 ('flexibility','How does formulative design compare with descriptive/diagnostic design in flexibility?','Formulative is flexible; descriptive/diagnostic is relatively fixed',['Both must be completely unplanned','Descriptive is flexible; formulative is fixed','Neither permits any decisions']),
 ('sampling-style','Which sampling contrast appears in the page 77 comparison?','Judgmental for formulative; random for descriptive/diagnostic',['Random for formulative; judgmental for descriptive','Both use no sampling','Both require a census']),
 ('analysis-planning','Which analysis-planning contrast appears on page 77?','No predetermined analysis design versus predetermined analysis design',['Both forbid analysis','Both require a final answer before inquiry','Both use identical analysis plans in every study']),
 ('operations','Which operational-planning contrast appears on page 77?','No fixed operational decision versus advanced decisions',['No procedures are allowed in either','Both wait until publication to decide','Operational decisions concern typography only']),
]:add('designs','contrast-'+key,f'According to the comparison on Methods of Research, PDF page 77, {prompt[0].lower()+prompt[1:]}',ans,wrong,[77],
 'This preserves the contrasts in the course table; they describe these design categories in this deck rather than rules binding every real study.')
design_rows=[
 ('experiment','Experimental','Tests cause/effect relationships with high control in a current study'),
 ('quasi','Quasi-experimental','Tests cause/effect relationships without full control, with moderate-to-high control'),
 ('cross-correlation','Non-experimental correlational (cross-sectional/past)','Examines relationships between variables in current or past observations'),
 ('expost','Ex post facto','Examines how a past event relates to current functioning'),
 ('predictive','Non-experimental correlational (predictive)','Examines relationships where a variable is measured later to make a prediction'),
 ('cohort','Cohort-sequential','Examines change in a variable over time in overlapping groups'),
 ('survey','Survey','Assesses opinions or characteristics existing at a given time'),
 ('qualitative','Qualitative','Discovers or describes potential relationships and lived experiences'),
]
identify('designs',design_rows,[78,79],prefix='Which research approach in the comparison tables')
for key,prompt,ans,wrong,pages in [
 ('experiment-example','Comparing two treatments for anxiety illustrates which row of the comparison table?','Experimental',['Survey','Qualitative','Cohort-sequential'],[78]),
 ('quasi-example','The table places gender differences in visual/spatial abilities under which row?','Quasi-experimental',['Randomized true experiment','Survey','Historical'],[78]),
 ('study-grade','A relationship between studying style and grade average is the example of which approach?','Non-experimental correlational',['Experimental','Historical source criticism','KR-20 computation'],[78]),
 ('abuse-example','A relationship between history of child abuse and depression illustrates which approach in the table?','Ex post facto',['Randomized intervention','Survey of voting preferences','Split-half analysis'],[78]),
 ('future-example','History of depression and later cancer development illustrates which table approach?','Predictive non-experimental correlation',['Static-group intervention','Historical criticism','Qualitative case description'],[79]),
 ('cohort-example','Examining how mother-child negativity changes over time illustrates which table approach?','Cohort-sequential',['One-shot case study','Concurrent validity','Action research only'],[79]),
 ('vote-example','Asking voting preferences before an election illustrates which approach?','Survey',['Randomized experiment','KR-20 reliability','Source-authenticity testing'],[79]),
 ('quit-example','Studying people\'s experiences of quitting smoking illustrates which table approach?','Qualitative',['Randomized treatment comparison','Parallel-forms reliability','Statistical design only'],[79]),
]:
 note='The table labels this gender-difference example quasi-experimental. Comparing pre-existing groups without an intervention is often causal-comparative/non-experimental; group differences alone do not make a true experiment.' if key=='quasi-example' else None
 add('designs',key,prompt,ans,wrong,pages,f'The supplied table uses this example for {ans.lower()}.',kind='application',note=note,refs=('quasi',) if note else ())

# HISTORICAL research, all source categories, examples and criticism questions.
add('historical','definition','What is historical research?',
 'Systematic collection and evaluation of evidence to describe, explain, and understand past events',
 ['Manipulating a treatment in every case','Measuring only future events without records','Choosing an answer without evaluating sources'],[81],
 'Historical research focuses on past occurrences and events, using collected evidence critically.')
add('historical','advantage-evidence','Which advantage is listed for historical research?',
 'It can study evidence from the past',['It requires no source evaluation','It eliminates bias automatically','It must manipulate historical events'],[81],
 'The slide emphasizes access to past evidence and a wider range of evidence.')
add('historical','advantage-range','What evidence advantage is named on page 81?',
 'A wider range of evidence than many other methods',['Only evidence from one questionnaire','No use of documents','Only present experimental scores'],[81],
 'Historical research may combine documents, numerical records, oral statements, and relics.')
add('historical','limitations','Which limitations does page 81 name?',
 'Bias and limited ability to use the usual controls for internal-validity threats',
 ['Too much experimental manipulation and no documents','Only expensive laboratory equipment','No relation to past events'],[81],
 'The slide notes bias and the impossibility of applying some controls used in other designs to past events.')
identify('historical',[
 ('learn','Learning from past successes and failures','Makes people aware of past events so they can learn from them'),
 ('apply','Applying past practices to present problems','Examines earlier ways of doing things for present-day use'),
 ('predict','Assisting prediction','Uses knowledge of the past to assist prediction'),
 ('trends','Testing relationships or trends','Tests hypotheses concerning relationships or trends'),
],[82],prefix='Which use of historical research')
historical_steps=['Defining the problem','Locating relevant sources','Summarizing information obtained from historical sources','Evaluating historical sources']
for i,ans in enumerate(historical_steps):
 add('historical',f'step-{i+1}',f'What is major step {i+1} in the historical-design slides?',ans,[x for x in historical_steps if x!=ans],[83] if i<2 else [86],f'The historical-design slides list this as step {i+1}: {ans.lower()}.')
identify('historical',[
 ('documents','Documents','Includes written or printed reports, books, records, diaries, newspapers, letters, and similar materials'),
 ('numbers','Numerical records','Includes scores, attendance figures, census reports, budgets, and similar quantitative records'),
 ('oral','Oral statements','Includes orally transmitted myths, legends, chants, songs, and stories'),
 ('relics','Relics','Includes physical or visual remains such as furniture, artwork, buildings, monuments, or equipment'),
],[83,84],prefix='Which historical-source category')
primary_examples=[('teacher','A nineteenth-century teacher\'s account of living with a frontier family'),('photo','A photograph of an eighth-grade class in 1930'),('essays','Students\' own essays about what they like and dislike about school'),('minutes','Minutes taken by the school board\'s secretary'),('songs','Songs composed by members of a high-school glee club')]
for key,item in primary_examples:
 add('historical','primary-'+key,f'How is this classified on page 85: {item}?','Primary source',['Secondary source','A sampling method','A reliability coefficient'],[85],
 'The example supplies direct evidence created by a participant or observer. Classify the evidence in relation to the research question.')
secondary_examples=[('encyclopedia','An encyclopedia describing a decade of educational research'),('aristotle','A magazine article summarizing Aristotle\'s views on education'),('teacher-report','A student\'s report of why her teacher said she was being suspended'),('colonies','A book describing schooling in the New England colonies during the 1700s'),('newspaper','A newspaper account of a board meeting based on interviews with board members')]
for key,item in secondary_examples:
 add('historical','secondary-'+key,f'According to the examples on Methods of Research, PDF page 85, how is this classified: {item}?','Secondary source',['Primary source','An experimental treatment','A conceptual framework'],[85],
 'The slide treats this as an account discussing or relaying evidence rather than the original firsthand record. Source status depends on what is being investigated.')
add('historical','external','What does external criticism of a historical source examine?',
 'The genuineness or authenticity of the document',['Only whether its claims support the desired conclusion','Only the sample standard deviation','Only the direction of a correlation'],[86,87],
 'External criticism establishes authenticity before the information within a source is evaluated.')
add('historical','internal','What does internal criticism examine after authenticity is established?',
 'Accuracy and truthfulness of the information and the author\'s account',
 ['Only whether the paper is genuine','Only the cover-page format','Only the publication price'],[87],
 'Internal criticism evaluates what the document says and the reliability of the account.')
for key,prompt,ans,wrong in [
 ('writer','Which external-criticism question concerns authorship?','Who wrote it, and was the author alive at the time?',['What is the item variance?','How many experimental treatments were used?','What is the final grade average?']),
 ('purpose','Which external-criticism question concerns the document\'s intended use?','For what purpose and audience was it written?',['Which coefficient exceeds 0.90?','How many pupils passed item 1?','What is the intervention effect size?']),
 ('date','Which external-criticism question checks the date?','When was it written, and is the stated date accurate?',['What was the questionnaire response rate?','What is the length of the test?','Which group received a posttest?']),
 ('place','Which external-criticism question checks the location?','Where was it written, and could its details have occurred there?',['Which hypothesis is null?','What is the KR-20 correction factor?','How many ranks are tied?']),
 ('conditions','Which question checks possible coercion or censorship?','Under what conditions was it written; could it have been censored?',['What is the student\'s test rank?','Which title has 20 words?','What is the confidence interval?']),
 ('versions','Which question checks textual consistency across records?','Do different forms or versions of the document exist?',['What is the number of study hours?','Which sample is randomized?','What is the variance ratio?']),
]:add('historical','external-'+key,prompt,ans,wrong,[86] if key in ['writer','purpose','date','place'] else [87],f'The slide includes this authenticity question under external criticism: {ans}')
for key,prompt,ans,wrong in [
 ('present','Which internal-criticism question concerns firsthand access?','Was the author present at the event?',['How thick is the paper?','Which edition has the newest cover?','What is the test-retest interval?']),
 ('role','Which internal-criticism question concerns the author\'s role?','Was the author a participant in or observer of the event?',['How many items are dichotomous?','Which question uses a nominal variable?','What is the sample variance?']),
 ('competent','Which internal-criticism question concerns the author\'s capability?','Was the author competent to describe the event?',['What was the paper\'s purchase price?','Which font was used?','How many test forms were printed?']),
]:add('historical','internal-'+key,prompt,ans,wrong,[87],f'Internal criticism includes asking: {ans}')

# DESCRIPTIVE research, values and all named subtypes.
add('descriptive','definition','What is the central purpose of descriptive research?',
 'Describe and interpret existing conditions, characteristics, relationships, or processes',
 ['Manipulate a treatment in every study','Guarantee a cause-and-effect conclusion','Study only past documents'],[89,90],
 'Descriptive research reports what exists and interprets the observations; it is more than merely accumulating facts.')
add('descriptive','forms','Can descriptive research be quantitative or qualitative?',
 'Yes; the slides explicitly allow either',['No; it always requires numerical manipulation','No; it always excludes numerical data','No; it must always be historical'],[90],
 'Page 90 describes both tabulated numerical descriptions and narrative descriptions of cases.')
add('descriptive','visual','Why are graphs and charts useful in descriptive research?',
 'They help readers understand the distribution of data',['They prove causation without a design','They replace the need for data','They guarantee unbiased sampling'],[90],
 'The slide explains that visual aids assist interpretation and that descriptive statistics reduce large amounts of data to manageable form.')
add('descriptive','areas','Which two broad areas of quantitative description are named on page 90?',
 'Describing events and drawing inferences or causal relationships',
 ['Only title writing and bibliography formatting','Only historical authenticity and oral records','Only financial planning and procurement'],[90],
 'This is the slide\'s two-area wording.',note='Description or observed association alone does not establish causation. Causal conclusions require a design and assumptions that address alternative explanations.',refs=('validity',))
values=[
 ('judgment','Facts for professional judgment','Provides facts on which professional judgments may be based'),
 ('insight','Insight into reality','Offers insight into the nature of what is being studied'),
 ('hypotheses','Forming hypotheses','Helps fashion hypotheses for further investigation'),
 ('norms','Establishing standard norms','Helps establish norms of conduct, behavior, or performance and improve tools'),
 ('remedy','Revealing problems for remedial action','Identifies abnormal conditions or problems so remedies can be considered'),
 ('prediction','Prediction from trends and correlations','Uses prevailing conditions, correlations, and trends to anticipate future conditions'),
 ('decision','Basis for decision making','Provides a basis for making decisions'),
]
identify('descriptive',values,[91],prefix='Which value of descriptive studies')
descriptive_types=[
 ('survey','Descriptive survey method','Looks at current conditions, analyzes and interprets their status'),
 ('normative','Descriptive normative method','Compares existing data with standards or norms'),
 ('correlational','Descriptive correlational method','Examines whether quantifiable variables are related, including direction and strength'),
 ('evaluative','Descriptive evaluative method','Judges the goodness, effectiveness, desirability, or worth of a program'),
 ('assessment','Descriptive assessment method','Describes existing conditions, practices, or beliefs without proposing or testing a hypothesis'),
 ('trend','Descriptive trend and perspective method','Uses recorded longitudinal data to infer what may happen in the future'),
 ('expost','Descriptive ex post facto method','Studies possible causal factors after a condition already exists'),
 ('case','Descriptive case study method','Studies a single typical or atypical individual, family, group, or situation intensively'),
 ('comparative','Descriptive comparative method','Examines relationships, similarities, or differences among variables'),
]
for i,(key,term,definition) in enumerate(descriptive_types):
 peers=[r[1] for r in descriptive_types if r[1]!=term]
 add('descriptive',key,f'Which descriptive method {definition[0].lower()+definition[1:]}?',term,[peers[(i+j)%len(peers)] for j in range(3)],[92] if i<4 else [93] if i<8 else [94],definition+'.')
add('descriptive','correlation-direction','What does a positive or negative correlation indicate in the descriptive-correlational slide?',
 'The direction of the relationship',['The authenticity of a document','The number of experimental groups','The publication order of sources'],[92],
 'The slide distinguishes whether there is a relationship, its direction (positive/negative), and its degree or strength.')
add('descriptive','expost-alias','What other name does the slide use for ex post facto research?',
 'Causal-comparative or after-the-fact research',['Randomized posttest-only experiment','Split-half measurement','External criticism'],[93],
 'Ex post facto examines an already-existing condition and possible antecedent factors; it does not create a past treatment.')
add('descriptive','genetic-heading','Which heading accompanies the paragraph called a genetic method on Methods of Research, PDF page 94?',
 'Descriptive Comparative Method',['Descriptive Survey Method','Descriptive Normative Method','Descriptive Assessment Method'],[94],
 'The yellow box is headed Descriptive Comparative Method but describes development over long periods and calls it genetic.',
 note='The yellow paragraph appears mismatched with its heading: longitudinal development is different from the green box\'s comparison of similarities and differences. Use the quoted heading only for this source-specific item; do not infer that every comparative study is developmental.',refs=('comparison',))
for key,prompt,ans,wrong in [
 ('adv-intervening','Which advantage of comparative studies concerns other influences?','Intervening variables can be noted and discerned',['All confounding is automatically removed','No other influence can ever exist','The researcher must manipulate every variable']),
 ('adv-select','Which advantage concerns choosing study variables?','Research variables can easily be selected',['No variables are needed','Variables must all be identical','Only one variable may ever be recorded']),
 ('adv-results','What does the slide say about access to comparative results?','They can be known immediately',['They are impossible to interpret','They always require centuries','They replace all data collection']),
 ('adv-conduct','Which practical advantage is stated for the comparative method?','It is easily conducted',['It eliminates every research cost','It guarantees causation','It never requires a sample']),
 ('limit-cause','What causal limitation is stated for comparative studies?','They cannot by themselves show the cause of change in another variable',['They always prove the treatment caused change','They always eliminate alternative explanations','They manipulate all influences randomly']),
 ('limit-vars','What variable-selection limitation is stated?','Variables available for selection may be limited',['Every possible variable is always available','Variables must never be named','No comparisons are permitted']),
 ('limit-sample','What sampling difficulty is stated for comparative studies?','Obtaining samples with the same characteristics or attributes',['Obtaining paper for a title page only','Finding a universal dictionary meaning','Choosing the final font size']),
]:add('descriptive','comparative-'+key,'According to the advantages/disadvantages list on Methods of Research, PDF page 94, '+prompt[0].lower()+prompt[1:],ans,wrong,[94],f'The slide lists: {ans}. These are the source\'s general statements, not guarantees for every study.')

# EXPERIMENTAL research and every plan step / design diagram.
add('experimental','definition','Which activity is essential to experimental design?',
 'Manipulation and control of independent variables to examine changes in outcomes',
 ['Only collecting existing records without an intervention','Only compiling a bibliography','Only asking about existing preferences'],[96,97],
 'Experimental research involves deliberately varying an independent variable and observing the dependent response.')
add('experimental','dependent-wording','Which wording appears in the third definition box on Methods of Research, PDF page 96?',
 'Manipulation of independent variables concomitant to manipulation of the dependent variable',
 ['No independent variable is manipulated','No variables are measured','Only a bibliography is manipulated'],[96],
 'The third box uses the word manipulation for the dependent variable.',note='The independent variable is manipulated; the dependent variable is ordinarily measured as the response. The slide\'s dependent-variable wording should not be used as a general definition.',refs=('validity',))
add('experimental','purpose','What does experimental research seek to examine?',
 'What caused a change in participants\' behavior or characteristics and what effect resulted',
 ['Only how a title should be centered','Only whether a historical document is genuine','Only the number of references in a paper'],[96],
 'The slide emphasizes examining changes and effects under controlled conditions.')
add('experimental','uses','Which research goals can use experimental design according to page 96?',
 'Basic, applied, or developmental research',['Only historical research','Only literature compilation','Only survey description'],[96],
 'The definition slide explicitly permits basic, applied, and developmental experimental work.')
identify('experimental',[
 ('control','Control group','Receives usual conditions, no experimental factor, or a comparison treatment'),
 ('experimental','Experimental group','Is exposed to the intervention or factor under consideration'),
 ('treatment','Treatment','Is the condition under which experimental and control groups are placed'),
 ('experiment','Experiment','Examines a hypothesis through an experimentally arranged study'),
],[75,97],prefix='Which experimental term')
add('experimental','lab-field','Where may an experiment reveal cause/effect relationships according to page 97?',
 'In the field or laboratory',['Only in printed bibliographies','Only in historical archives','Only in a classroom with no intervention'],[97],
 'The slide allows experiments in both field and laboratory settings.')
add('experimental','funding','What institutional consideration is stated on page 97?',
 'Research institutions may prioritize experimental work in grants-in-aid',
 ['All funding is guaranteed','Experiments never need money','Every other method is prohibited'],[97],
 'This is the slide\'s statement about institutional priority; it is not a promise about any particular grant.')
add('experimental','harvest','Which principle is named on the distinguishing-features slide?',
 'Invest-harvest principle',['Random-format principle','Primary-source-only principle','Rank-preservation principle'],[97],
 'Page 97 names the invest-harvest principle without explaining it. The question tests the label only; no unsupported definition is added.')
ms=['Manpower','Money','Methods','Materials','Machinery','Moment of time','Marketing']
for i,m in enumerate(ms):
 add('experimental',f'm-{i+1}',f'Which of the 7 Ms on page 98 refers to '+['people carrying out the work','financial resources','procedures used','consumable resources','equipment or machines','the time dimension','dissemination or market-facing activity in the mnemonic'][i]+'?',m,[ms[(i+d)%7] for d in [1,2,3]],[98],f'{m} is one of the seven labels: '+', '.join(ms)+'.')
plan=['Determining the experimental problem or topic','Surveying related literature and studies','Formulating hypotheses','Identifying experimental variables','Selecting the appropriate experimental design','Selecting the sample','Selecting or constructing appropriate measurement instruments','Conducting the experiment','Measuring results and applying statistical procedures','Writing the experimental report']
for i,step in enumerate(plan):
 add('experimental',f'plan-{i+1}',f'What is step {i+1} in the experimental plan on PDF page 99?',step,[plan[(i+d)%10] for d in [2,4,6]],[99],f'The experimental plan lists step {i+1} as {step.lower()}.')
threats=[('history','History','An outside event occurs during the study'),('maturation','Maturation','Participants change naturally over time'),('testing','Testing','An earlier test affects later performance'),('selection','Selection bias','Groups differ because of how respondents are selected'),('mortality','Experimental mortality','Participants drop out of the study'),('interaction','Interaction effects','Influences combine rather than operating separately')]
identify('experimental',threats,[99],prefix='Which threat listed under conducting an experiment is illustrated when')
design_patterns=[
 ('one-shot','Posttest-only / one-shot case study','One group receives a treatment followed by one observation; there is no pretest or control group',[100],'X  O'),
 ('one-prepost','One-group pretest-posttest design','One group is observed before and after treatment, without a separate control group',[100],'O1  X  O2'),
 ('static','Static-group comparison design','An existing treated group and a comparison group are observed after the treatment',[101],'Experimental: X  O\nControl:          O'),
 ('random-prepost','Pretest-posttest control-group design','Randomly assigned experimental and control groups both have pretests and posttests',[101],'R Experimental: O1  X  O2\nR Control:      O3     O4'),
 ('random-post','Posttest-only control-group design','Randomly assigned experimental and control groups receive only posttests',[102],'R Experimental: X  O1\nR Control:         O2'),
 ('solomon','Solomon four-group design','Four randomized groups are used; one experimental and one control group have pretests, and all four have posttests',[102],'R Experimental: O1  X  O2\nR Control:      O3     O4\nR Experimental:     X  O5\nR Control:            O6'),
 ('nonequivalent','Non-equivalent control-group design','Experimental and control groups both have pretests and posttests but are not randomly assigned',[103],'Experimental: O1  X  O2\nControl:      O3     O4'),
 ('separate','Separate-sample pretest-posttest group design','One sample supplies the baseline pretest and another supplies the posttest',[103],'Pretest sample:  O1\nPosttest sample:         O2'),
 ('time-series','Time-series design','One group is measured repeatedly before and after an intervention',[104],'O1  O2  O3  O4  X  O5  O6  O7  O8'),
]
for i,(key,term,definition,pages,diagram) in enumerate(design_patterns):
 peers=[r[1] for r in design_patterns if r[1]!=term]
 add('experimental','design-'+key,f'Which design matches this description: {definition[0].lower()+definition[1:]}?',term,[peers[(i+j)%8] for j in range(3)],pages,definition+'.',kind='application')
 if key!='separate':
  add('experimental','diagram-'+key,'Which design is represented by this notation?',term,[peers[(i+j+2)%8] for j in range(3)],pages,
      'X indicates treatment; O indicates observation; R indicates random assignment. '+definition+'.',diagram=diagram,kind='diagram',
      note='The printed control row on page 103 also shows X, contradicting the text\'s control comparison. This question uses the stated design description and clearly labels a corrected schematic; the control row is shown without the intervention.' if key=='nonequivalent' else None,
      refs=('quasi','comparison') if key=='nonequivalent' else (),diagramLabel='Corrected schematic from the stated design description' if key=='nonequivalent' else 'Slide notation transcribed into text')
add('experimental','notation-x','What does X denote in the experimental-design diagrams?', 'Treatment or intervention',['An observation only','Random assignment','A bibliography entry'],[100,101,102,103,104], 'X marks the intervention; observations are shown by O and random assignment by R.')
add('experimental','notation-o','What does O denote in the experimental-design diagrams?', 'An observation or measurement',['Random assignment','The intervention itself','A funding source'],[100,101,102,103,104], 'O marks an observation; numbered observations identify distinct measurements.')
add('experimental','notation-r','What does R indicate in the randomized control-group diagrams?', 'Random assignment',['A reliability score','A review of related literature','A recommendation'],[101,102], 'R precedes the randomized groups in the true-experimental diagrams.')
add('experimental','nonequivalent-printed','What appears in BOTH rows of the non-equivalent design diagram printed on Methods of Research, PDF page 103?',
 'X, the treatment symbol',['R, the random-assignment symbol','No observation symbols','Only one O symbol total'],[103],
 'The printed schematic contains X in both the experimental and control rows.',note='This conflicts with the text\'s control-group comparison. A conventional untreated comparison row does not receive the intervention X. Do not copy the printed extra X into a corrected comparison diagram.',refs=('comparison',))
add('experimental','separate-printed','According to the text on Methods of Research, PDF page 103, how are pretest and posttest measurements obtained in the separate-sample design?',
 'From different groups or samples',['From one identical group measured at every occasion','From four groups all given pretests','From no sample at all'],[103],
 'The text says one group supplies the baseline and another the posttest.',note='The separate-sample sketch has ambiguous X placement and mixes random selection wording with R notation. The bank tests the readable prose and does not score an exact reconstruction of that ambiguous sketch.',refs=('comparison',))
add('experimental','time-count','In the page 104 time-series diagram, how many observations occur on each side of X?',
 'Four before and four after',['One before and one after','Two before and six after','Eight before and none after'],[104],
 'O1-O4 precede X and O5-O8 follow it. Repeated observations help reveal trends that a single pretest/posttest pair may miss.',kind='diagram',diagram=design_patterns[-1][-1])

# ARCHITECTURE OF INQUIRY: all visual elements of the 15-page deck.
add('approaches','architecture-equation','What is the output of the Method + Action + Output diagram ultimately intended to support?',
 'Societal mobilization, informed action, and translation into policy/practice',
 ['Only completing a course prerequisite','Avoiding evidence-based action','Replacing inquiry with authority'],[2],
 'The diagram combines systematic inquiry, searching/validating/refining/generating, and objective knowledge/evidence to support action.',source='architecture')
for key,prompt,ans,wrong in [
 ('method','Which part of the page 2 diagram describes systematic, disciplined, scientific, empirical inquiry?','The Method',['The Action','The Output','The dissemination medium']),
 ('action','Which part describes searching, validating, refining, and generating?','The Action',['The Method','The Output','The sample']),
 ('output','Which part describes objective knowledge, truth, and evidence?','The Output',['The Method','The Action','The instrument cost']),
]:add('approaches',key,prompt,ans,wrong,[2],f'Page 2 assigns this description to {ans.lower()}.',source='architecture')
pillars=[('controlled','Controlled','Minimizes effects of extraneous variables'),('rigorous','Rigorous','Uses relevant, appropriate, justified procedures'),('systematic','Systematic','Follows a logical, deliberate, planned sequence'),('valid','Valid and verifiable','Has findings that are correct and reproducible by others'),('empirical','Empirical','Is grounded in evidence and real-life observation'),('critical','Critical','Withstands scrutiny and questions its own claims'),('transparent','Transparent','States methods, assumptions, and data explicitly')]
identify('approaches',pillars,[3],source='architecture',prefix='Which pillar of rigorous research')
professional=[('evidence','Evidence-based practice','Bases professional practice on evidence'),('credibility','Professional credibility','Establishes credibility in a profession'),('accountability','Accountability','Requires responsibility for professional actions'),('cost','Cost-effectiveness through documentation','Uses documentation to improve cost-effectiveness')]
identify('approaches',professional,[4],source='architecture',prefix='Which professional goal')
for key,prompt,ans,wrong in [
 ('exploratory','Which investigative purpose formulates precise questions and navigates the unknown?','Exploratory',['Descriptive','Explanatory','Summative evaluation']),
 ('descriptive','Which purpose presents the Who, What, Where, and How?','Descriptive',['Exploratory','Explanatory','Instrument validation']),
 ('explanatory','Which purpose examines underlying causes and the Why?','Explanatory',['Descriptive','Exploratory','Title formatting']),
]:add('approaches','purpose-'+key,prompt,ans,wrong,[4],f'The investigative-purpose diagram associates this function with {ans.lower()} inquiry.',source='architecture')
add('approaches','basic','What is the goal of basic research?', 'Advance fundamental knowledge and support or refute theories',
 ['Solve only an immediate practical task','Produce only a classroom ranking','Avoid theoretical questions'],[5],
 'Basic research focuses on fundamental understanding; its primary consumer in the slide is the academic community.',source='architecture',extra=({'sourceId':'methods','pages':[21]},))
add('approaches','applied','What is the goal of applied research?', 'Solve specific problems or accomplish practical tasks',
 ['Avoid all practical questions','Only reproduce a theory title','Replace evidence with personal authority'],[5],
 'Applied research emphasizes immediate practical use and serves practitioners, decision-makers, and teachers.',source='architecture',extra=({'sourceId':'methods','pages':[21]},))
add('approaches','basic-consumer','Who is the primary consumer of basic research in the page 5 comparison?', 'The academic community',
 ['Only product vendors','Only respondents taking a test','Only a local procurement team'],[5],
 'The basic-research column names the academic community; the applied column names practitioners and decision-makers.',source='architecture')
add('approaches','applied-consumer','Who is the primary consumer of applied research in the comparison?', 'Practitioners, decision-makers, and teachers',
 ['Only the academic theory community','Only the test publisher','Only archival conservators'],[5],
 'Applied research is oriented toward people who use findings for practical tasks.',source='architecture')
add('approaches','same-methods','What does the slide emphasize about basic and applied research methods?',
 'They differ in application rather than in commitment to scientific inquiry',
 ['Applied research does not require evidence','Basic research cannot use analysis','They must always use incompatible methods'],[5],
 'The slide says both employ rigorous scientific methods and analytical techniques, despite their different goals.',source='architecture')
for key,prompt,ans,wrong in [
 ('action-research','Which applied approach is conducted by/for practitioners to improve their own actions?','Action research',['Impact assessment','Summative evaluation','Historical criticism']),
 ('impact','Which approach estimates consequences of a planned change or policy?','Impact assessment',['Action research','Conceptual definition','External criticism']),
 ('evaluation','Which approach establishes value judgments?','Evaluation',['Test-retest correlation','Source authentication','Variable coding']),
 ('formative','Which evaluation is described as ongoing monitoring?','Formative evaluation',['Summative evaluation','Parallel-forms reliability','Historical analysis']),
 ('summative','Which evaluation concerns final outcomes?','Summative evaluation',['Formative evaluation','Test-retest reliability','Conceptual definition']),
 ('cross','Which time design studies a single fixed time point?','Cross-sectional',['Longitudinal','Time-series intervention','Cohort panel follow-up']),
 ('long','Which time design observes multiple time points over an extended period?','Longitudinal',['Cross-sectional','One-shot posttest-only','Single-date survey']),
 ('long-types','Which examples are named for longitudinal research?','Time series, panel, and cohort',['Dictionary, almanac, and encyclopedia','Null, alternative, and assumption','Content, concurrent, and construct validity']),
 ('cross-limit','What trade-off is stated for cross-sectional research?','It is cost-effective but cannot directly capture the process of change',['It always proves changes over time','It requires decades of repeated measurements','It can never use a questionnaire']),
 ('long-limit','What trade-off is stated for longitudinal research?','It can analyze change but is costly',['It needs no repeated observations','It cannot examine change','It is defined by one fixed time point']),
]:add('approaches',key,prompt,ans,wrong,[6],f'The applied-interventions/time-dimension slide states: {ans}.',source='architecture')
for key,prompt,ans,wrong in [
 ('quant','Which methodological domain emphasizes deduction, numbers, objective reality, and statistical analysis?','Quantitative research',['Qualitative research','Historical criticism only','Literature formatting']),
 ('qual','Which domain emphasizes induction, subjective experience, human behavior, and natural settings?','Qualitative research',['Quantitative research','Instrument scoring only','Randomized allocation only']),
 ('mixed','Which domain combines quantitative and qualitative paradigms?','Mixed methods',['A single-method survey only','A single archival document only','A numerical calculation only']),
]:add('approaches','domain-'+key,prompt,ans,wrong,[7],f'The page 7 domain diagram associates these features with {ans.lower()}.',source='architecture')
for key,prompt,ans,wrong in [
 ('survey','Which quantitative approach uses questionnaires or interviews to describe behavior across groups?','Survey',['Experimental','Causal-comparative','Historical criticism']),
 ('correlation','Which approach examines relationships between two or more variables without implying causation?','Correlational',['Experimental manipulation','Source authentication','Conceptual definition']),
 ('causal-comparative','Which approach compares differently affected groups without manipulating variables?','Causal-comparative',['Randomized experiment','Test-retest','Document authentication']),
 ('experimental','Which approach directly manipulates and controls variables under a hypothesis?','Experimental',['Correlational','Survey only','Causal-comparative']),
]:add('approaches','quant-'+key,prompt,ans,wrong,[8],f'The quantitative-research slide names {ans.lower()} for this description.',source='architecture')
add('approaches','correlation-caution','What warning accompanies correlational research?', 'Correlation does not establish causation',
 ['Any correlation proves causation','Only negative correlation is causal','Two variables cannot be correlated'],[8],
 'The slide explicitly cautions against interpreting an association as proof of cause and effect.',source='architecture')
for key,prompt,ans,wrong in [
 ('true','Which designs are listed under TRUE EXPERIMENTAL on page 9?','Pretest-posttest and Solomon four-group',['Non-equivalent groups and time series','One-shot case and one-group pretest','Survey and meta-analysis']),
 ('quasi','Which designs are listed under QUASI-EXPERIMENTAL?','Non-equivalent groups and time series',['Solomon four-group and randomized pretest-posttest','One-shot case and one-group pretest','Survey and comparative research']),
 ('pre','Which designs are listed under PRE-EXPERIMENTAL?','One-shot case and one-group pretest',['Solomon four-group and randomized control groups','Panel and cohort only','Meta-analysis and survey']),
 ('nonexperiment','What distinguishes the non-experimental branch?','No manipulation of the study variables',['Required random assignment to a treatment','Mandatory four-group intervention','Only repeated treatment exposures']),
 ('non-types','Which list appears under non-experimental types?','Action, comparative, developmental, evaluation, meta-analysis, and survey',['Only Solomon and randomized pretest-posttest','Only test-retest and split-half','Only content and construct validity']),
]:add('approaches','classification-'+key,'According to The Architecture of Inquiry, PDF page 9, '+prompt[0].lower()+prompt[1:],ans,wrong,[9],
 'This question follows the classifications printed in this deck. A design\'s actual procedures determine its classification; broad labels such as action or evaluation can use more than one design.',source='architecture')
add('approaches','external-validity-slide','How does The Architecture of Inquiry, PDF page 9, describe EXTERNAL validity in its sidebar?',
 'Changes attributed to extraneous variables',['Generalizability to other people and settings','Agreement between alternate test forms','Proportion of items answered correctly'],[9],
 'The sidebar uses this wording, which is retained only as a source-specific expected answer.',source='architecture',
 note='External validity concerns generalization beyond the studied people/settings. Extraneous variables and alternative causes concern internal validity. The sidebar conflates these concepts.',refs=('validity',))
add('approaches','internal-validity-slide','How does the page 9 sidebar describe INTERNAL validity?',
 'Changes attributed to the independent variable',['Only generalization to another country','Only the number of questionnaire pages','Only scoring convenience'],[9],
 'The sidebar connects internal validity with attributing changes to the independent variable; alternative explanations must be addressed.',source='architecture')
add('approaches','naturalistic','What is the naturalistic lens in qualitative research?',
 'In-depth study of subjective human experience in natural settings',
 ['Only numerical measurement in every study','Only random assignment in a laboratory','Only a summary of unrelated books'],[10],
 'The slide emphasizes human complexity, natural settings, and open exploration rather than imposing an existing theory.',source='architecture')
for key,prompt,ans,wrong in [
 ('orientation','What is stage 1 of the qualitative process shown on page 10?','Orientation and overview',['Confirmation and closure','Final hypothesis rejection','Publication and dissemination']),
 ('focused','What is stage 2 of that qualitative process?','Focused exploration',['Orientation and overview','Immediate final conclusion','Random assignment']),
 ('closure','What is stage 3 of that qualitative process?','Confirmation and closure',['Initial source collection','Sample-size calculation','Unrestricted treatment allocation']),
 ('salient','What is determined during orientation and overview?','What is salient about the phenomenon',['The preferred conclusion before evidence','The final grant amount only','Every participant\'s test rank']),
 ('scrutiny','What guides focused exploration?','In-depth scrutiny based on the outcomes of phase 1',['A fixed final answer before observation','Only a published answer key','Elimination of all participant context']),
 ('trust','How does confirmation and closure establish trustworthiness on the slide?','By verifying findings with participants',['By ignoring participant accounts','By declaring all interpretations identical','By removing all contrary evidence']),
 ('limitations','Which limitations are explicitly listed for qualitative research on this slide?','Reductionist by nature, highly subjective, and limited to small samples',['Requires all data to be numerical','Always has no context','Always demands a randomized treatment']),
]:add('approaches','qual-'+key,'According to The Architecture of Inquiry, PDF page 10, '+prompt[0].lower()+prompt[1:],ans,wrong,[10],
 'This follows the labels and descriptions in the supplied qualitative-research slide. Its limitation list is a characterization in this deck, not a universal definition of every qualitative study.',source='architecture')
identify('approaches',[
 ('phenomenology','Phenomenology','Focuses on lived experiences and the subjective reality of individuals'),
 ('ethnography','Ethnography','Focuses on cultural characteristics through immersion and key informants'),
 ('history','Historical approach','Examines past events using primary/secondary evidence and internal/external criticism'),
 ('case-study','Case study','Observes a particular person, group, or event in depth over time using interviews, notes, and observation'),
],[11],source='architecture',prefix='Which qualitative approach')
add('approaches','phenomenology-flexible','What procedural feature does the phenomenology box emphasize?',
 'No rigidly defined sequence, allowing creativity',['Mandatory random assignment','Only one fixed numerical formula','No study of experience'],[11],
 'The slide associates phenomenology with lived experience, subjective reality, and flexible inquiry.',source='architecture')
identify('approaches',[
 ('triangulation','Triangulation','Corroborates results across different methods'),
 ('complementarity','Complementarity','Clarifies the results of one method using the other'),
 ('expansion','Expansion','Broadens the overall range of inquiry'),
 ('initiation','Initiation','Discovers paradoxes that help reframe research questions'),
 ('development','Development','Uses findings from one method to inform the other'),
],[12],source='architecture',prefix='Which mixed-methods purpose')
add('approaches','mixed-method-model','What design distinction is printed in the mixed-methods slide\'s note?',
 'Mixed Method splits paradigms by phase; Mixed Model mixes them within a single stage',
 ['Mixed Method prohibits qualitative evidence; Mixed Model prohibits numbers','Both mean only a survey','Both require four randomized groups'],[12],
 'This preserves the distinction and capitalization used in the source note.',source='architecture')

# e-RESEARCH: complete pyramid and traditional/digital comparison.
identify('digital',[
 ('cyber','Cyberinfrastructure','Provides the overarching computing and network environment enabling virtual e-science communities'),
 ('grid','Grid','Combines data repositories, specialized scientific equipment, and pooled computing power'),
 ('middleware','Middleware','Provides standard community software tools/services for knowledge sharing'),
 ('practice','e-Research (the practice)','Uses collaboration, advanced visualization, and global research-data management'),
],[13],source='architecture',prefix='Which layer of the infrastructure pyramid')
layers=['Cyberinfrastructure','Grid','Middleware','e-Research (the practice)']
for i,term in enumerate(layers):
 add('digital',f'layer-{i}',f'Which pyramid layer is position {i+1} counting from the BASE upward?',term,[x for x in layers if x!=term],[13],
 'From base to top: Cyberinfrastructure → Grid → Middleware → e-Research.',source='architecture',kind='diagram')
comparisons=[
 ('participants','Participants','Individual/local teams','Diversely skilled, distributed global teams'),
 ('data','Data','Locally generated and stored','Globally generated, stored, and accessible'),
 ('computation','Computation','Runs on researchers\' own local computers','Large-scale, on-demand computation and shared instruments'),
 ('networking','Networking','Not reliant on the internet','Reliant on internet and middleware'),
 ('dissemination','Dissemination','Print publications and physical conferences','Websites and specialized web portals'),
]
for key,term,old,new in comparisons:
 peers=[r[1] for r in comparisons if r[1]!=term]
 add('digital','dimension-'+key,f'Which dimension changes from "{old}" to "{new}" in the traditional/e-Research table?',term,peers[:3],[14],
 f'The slide contrasts {term.lower()}: traditional — {old}; e-Research — {new}. These are simplified contrasts, not exclusive possibilities.',source='architecture')
 add('digital','modern-'+key,f'According to the page 14 comparison, which describes e-Research {term.lower()}?',new,[old]+[r[3] for r in comparisons if r[1]!=term][:2],[14],
 f'The e-Research column lists: {new}.',source='architecture')
ecosystem=[('input','The Input','Purpose and goals: exploratory, descriptive, and explanatory'),('engine','The Engine','Quantitative, qualitative, mixed methods, and time dimensions'),('infrastructure','The Infrastructure','The e-Research cyberinfrastructure stack enabling global scale'),('output','The Output','Translation into evidence-based practice and societal mobilization')]
identify('digital',ecosystem,[15],source='architecture',prefix='Which stage of the modern research ecosystem contains')
add('digital','ecosystem-sequence','Which sequence follows the modern ecosystem diagram?',
 'Input → Engine → Infrastructure → Output',
 ['Output → Input → Infrastructure → Engine','Infrastructure → Output → Engine → Input','Engine → Output → Input → Infrastructure'],[15],
 'The four labeled stages move from purpose/goals through methodology and infrastructure to practical impact.',source='architecture',kind='diagram')

# RELIABILITY: concepts, formulas, data tables, all worked computation steps.
methods=[('retest','Test-retest','Estimates stability across repeated administrations of the same test'),('parallel','Parallel-forms','Estimates equivalence between alternate instruments'),('split','Split-half','Correlates parts of one test and corrects to full-test length'),('kr','KR-20 / internal consistency','Uses the Kuder-Richardson item-variance formula for dichotomously scored items')]
identify('reliability',methods,[2],source='reliability',prefix='Which reliability method',extra=({'sourceId':'methods','pages':[28]},))
add('reliability','retest-conditions','How is test-retest reliability estimated in the reliability deck?',
 'Administer the same instrument twice to the same group over a time interval',
 ['Administer unrelated tests to different people','Split two unrelated samples by age','Compare different constructs without paired observations'],[3],
 'The repeated measurements concern temporal stability in the same cohort.',source='reliability')
add('reliability','spearman-use','When does this deck use Spearman rank correlation for test-retest?',
 'When paired test results are expressed as ordinal rankings',
 ['Only when there is no paired information','Only when every score is a text label with no order','Only when all test items have identical difficulty'],[3],
 'The deck qualifies the formula for rank data. Do not interpret this as saying every test-retest study must use Spearman.',source='reliability')
add('reliability','spearman-formula','Which is the Spearman rank formula shown in the deck?',
 'rₛ = 1 − 6ΣD² / (N³ − N)',
 ['rₛ = 6ΣD² / N','rₛ = 2r / (1 + r)','rₛ = N / (N − 1)'],[3],
 'For the untied rankings used in the example, subtract 6 times the sum of squared rank differences divided by N³ − N from 1.',source='reliability',formula='rₛ = 1 − (6ΣD²)/(N³ − N)')
add('reliability','spearman-d','What does D represent in the Spearman formula?', 'Difference between a subject\'s two ranks',
 ['Difference between two sample sizes','The total variance of a test','The number of items'],[3,4],
 'D is the paired rank difference. Squaring removes its sign before summation.',source='reliability')
add('reliability','spearman-n','What does N represent in the Spearman example?', 'The number of paired participants',
 ['The number of test questions','The passing proportion','The variance of the test'],[3,4],
 'N is the sample size (five students in the worked example), unlike N in this deck\'s KR-20 formula, where it means item count.',source='reliability')
add('reliability','parallel-conditions','What is required for the parallel-forms method as presented?',
 'Two equivalent forms with matching blueprints administered to the same group',
 ['One test given once with no comparison','Different constructs measured in unrelated groups','Only odd-numbered items without a second form'],[5],
 'Paired scores on equivalent instruments are correlated to estimate form equivalence.',source='reliability')
add('reliability','pearson','Which correlation formula is used for the paired parallel-form scores?',
 'Pearson product-moment correlation',['Spearman-Brown prophecy correction','KR-20 alone','A frequency percentage only'],[5],
 'The parallel-forms example uses Pearson correlation between Form A (X) and Form B (Y).',source='reliability',
 formula='r = [NΣXY − (ΣX)(ΣY)] / √{[NΣX² − (ΣX)²][NΣY² − (ΣY)²]}')
add('reliability','pearson-xy','What do X and Y denote in the parallel-forms example?', 'Form A and Form B scores',
 ['Two rank differences only','Item count and sample size','Pass rate and fail rate'],[5,6],
 'Each row pairs one student\'s score on Form A with that same student\'s score on Form B.',source='reliability')
add('reliability','split-single','How is split-half reliability obtained in the reliability deck?',
 'Divide a single administered test into comparable halves and correlate half scores',
 ['Require two administrations of the identical full test','Administer unrelated forms to different groups','Correlate only unrelated bibliography entries'],[7],
 'The deck uses one administration, often partitioned into odd and even items.',source='reliability',extra=({'sourceId':'methods','pages':[28]},))
add('reliability','split-conflict','What administration wording appears for split-half in Methods of Research, PDF page 28?',
 'The test may be administered twice',['The test must never be administered','Only different groups can answer each half','The method requires three alternate instruments'],[28],
 'Page 28 states that the test may be administered twice.',note='Split-half reliability ordinarily uses one administration split into comparable halves. The supplied reliability deck page 7 uses that single-test approach. Two administrations are not required for split-half estimation.',refs=('split','spearman-brown'))
add('reliability','split-purpose','Why is the Spearman-Brown correction applied to the half-test correlation?',
 'To estimate reliability at the original full-test length',
 ['To replace all observed scores with ranks','To convert a sample size into a variance','To establish content validity directly'],[7,8],
 'Correlating halves concerns shorter tests; the correction estimates full-length reliability under its comparability assumptions.',source='reliability')
add('reliability','split-formula','Which formula corrects an equal-half correlation to whole-test reliability?',
 'rwt = 2rht / (1 + rht)', ['rwt = 1 − 6ΣD² / (N³ − N)','rwt = rht / 2','rwt = N / (N − 1)'],[7],
 'rht is half-test correlation; rwt is the estimated whole-test reliability.',source='reliability',formula='rwt = (2 × rht)/(1 + rht)')
add('reliability','kr-items','For what item scoring is KR-20 intended?', 'Dichotomous scoring such as right/wrong or 1/0',
 ['Only continuous essay scores without dichotomizing','Only unpaired ranks','Only text responses without scoring'],[9],
 'The deck describes KR-20 for item homogeneity/internal consistency in dichotomously scored tests.',source='reliability')
add('reliability','kr-formula','Which is the KR-20 formula shown in the deck?',
 'Rxx = [N/(N − 1)] × [(SD² − Σpq)/SD²]',
 ['Rxx = 2r/(1 + r)','Rxx = 1 − 6ΣD²/(N³ − N)','Rxx = Σpq × SD²'],[9],
 'The N/(N − 1) multiplier is applied to 1 minus the ratio of summed item variances to total-score variance.',source='reliability',formula='KR-20 = [N/(N − 1)] × [1 − Σpq/SD²]')
for key,prompt,ans,wrong in [
 ('n','What does N mean in this deck\'s KR-20 formula?','Number of test items',['Number of paired participants','Proportion passing an item','Difference in paired ranks']),
 ('p','What does p mean in KR-20?','Proportion answering an item correctly',['Total-score variance','Number of participants','Number of questions minus one']),
 ('q','What does q mean in KR-20?','Proportion answering incorrectly, equal to 1 − p',['The same value as N','Total-score standard deviation','The paired-score correlation']),
 ('variance','What does SD² denote in the KR-20 example?','Variance of total test scores',['The standard deviation without squaring','The number of test forms','The sum of the ranks']),
 ('pq','What does Σpq represent?','Sum of dichotomous item variances',['Total number of participants','Sum of paired test scores','Number of administrations']),
]:add('reliability','kr-'+key,prompt,ans,wrong,[9,10],f'The formula notation identifies {ans.lower()}.',source='reliability')
def calc(key,prompt,answer,wrong,pages,steps,method,inputs,formula=None,table=None):
    return add('reliability',key,prompt,answer,wrong,pages,'\n'.join(steps),source='reliability',kind='calculation',
               calculation={'method':method,'inputs':inputs,'expected':answer},**({'formula':formula} if formula else {}),**({'table':table} if table else {}))
ranks={'headers':['Student','Rank 1','Rank 2','D','D²'],'rows':[['A',1,1,0,0],['B',2,3,-1,1],['C',3,2,1,1],['D',4,4,0,0],['E',5,5,0,0]]}
calc('spearman-sum','Using the rank table, what is ΣD²? Give an exact whole number.','2',['0','1','4'],[4],['D² values are 0, 1, 1, 0, 0.','ΣD² = 0 + 1 + 1 + 0 + 0 = 2.'],'rank-sum',{'x':[1,2,3,4,5],'y':[1,3,2,4,5]},table=ranks)
calc('spearman-denominator','For N = 5, what is N³ − N? Give an exact whole number.','120',['20','125','25'],[4],['5³ − 5 = 125 − 5 = 120.'],'rank-denominator',{'n':5})
calc('spearman-numerator','If ΣD² = 2, what is 6ΣD²? Give an exact whole number.','12',['6','2','36'],[4],['6 × 2 = 12.'],'rank-numerator',{'sumD2':2})
calc('spearman-fraction','With N = 5 and ΣD² = 2, what fraction is subtracted from 1? Round to two decimal places.','0.10',['0.90','0.20','0.01'],[4],['6ΣD² = 12.','N³ − N = 120.','12/120 = 0.10.'],'rank-fraction',{'n':5,'sumD2':2})
calc('spearman-result','Using the table, what is Spearman rₛ? Round to two decimal places.','0.90',['0.10','0.80','1.00'],[4],['ΣD² = 2 and N = 5.','rₛ = 1 − (6 × 2)/(125 − 5).','rₛ = 1 − 12/120 = 0.90.'],'spearman',{'x':[1,2,3,4,5],'y':[1,3,2,4,5]},table=ranks,formula='rₛ = 1 − (6ΣD²)/(N³ − N)')
parallel_table={'headers':['Student','X','Y','X²','Y²','XY'],'rows':[[1,10,9,100,81,90],[2,8,8,64,64,64],[3,6,7,36,49,42],[4,5,4,25,16,20],[5,3,4,9,16,12]]}
paired={'x':[10,8,6,5,3],'y':[9,8,7,4,4]}
for key,label,ans,wrong,method in [
 ('x','ΣX','32',['30','34','64'],'sum-x'),('y','ΣY','32',['28','36','64'],'sum-y'),
 ('x2','ΣX²','234',['226','228','1024'],'sum-x2'),('y2','ΣY²','226',['234','228','1024'],'sum-y2'),
 ('xy','ΣXY','228',['234','226','1024'],'sum-xy')]:
 calc('pearson-total-'+key,f'From the parallel-form table, what is {label}? Give an exact whole number.',ans,wrong,[6],[f'Add the values in the {label[1:]} column: {label} = {ans}.'],method,paired,table=parallel_table)
calc('pearson-numerator','For N = 5, ΣXY = 228, and ΣX = ΣY = 32, what is the Pearson numerator? Give an exact whole number.',
 '116',['1140','1024','124'],[6],['NΣXY − ΣXΣY = 5(228) − 32(32).','1140 − 1024 = 116.'],'pearson-numerator',paired)
calc('pearson-denominator','With N = 5, ΣX² = 234, ΣY² = 226, and ΣX = ΣY = 32, what is the Pearson denominator? Round to two decimals.',
 '124.40',['116.00','15476.00','126.00'],[6],['√[(5×234 − 32²)(5×226 − 32²)]','= √[(1170−1024)(1130−1024)]','= √(146×106) = √15476 ≈ 124.40.'],'pearson-denominator',paired)
calc('pearson-result','What is Pearson r for the parallel-form scores in the table? Round to two decimal places.',
 '0.93',['0.90','0.82','0.67'],[6],['Numerator = 116.','Denominator = √15476 ≈ 124.4026.','r = 116/124.4026 ≈ 0.93246 → 0.93.'],'pearson',paired,table=parallel_table)
calc('split-numerator','For half-test correlation rht = 0.70, what is 2rht? Round to two decimal places.',
 '1.40',['0.35','1.70','0.70'],[8],['2 × 0.70 = 1.40.'],'split-numerator',{'r':0.7})
calc('split-denominator','For rht = 0.70, what is 1 + rht? Round to two decimal places.',
 '1.70',['1.40','0.30','0.70'],[8],['1 + 0.70 = 1.70.'],'split-denominator',{'r':0.7})
calc('split-result','A test has an odd-even half correlation of 0.70. What is its corrected whole-test reliability? Round to two decimals.',
 '0.82',['0.70','0.35','1.40'],[8],['rwt = 2(0.70)/(1 + 0.70).','= 1.40/1.70 = 0.823529…','Rounded to two decimals: 0.82.'],'split',{'r':0.7},formula='rwt = (2 × rht)/(1 + rht)')
calc('kr-multiplier','For a 10-item test, what is N/(N − 1)? Round to three decimal places.',
 '1.111',['0.900','1.000','0.111'],[10],['10/(10 − 1) = 10/9 = 1.111111…','To three decimals: 1.111.'],'kr-multiplier',{'n':10})
calc('kr-ratio','If total-score variance is 4.00 and Σpq = 1.60, what is (SD² − Σpq)/SD²? Round to three decimals.',
 '0.600',['0.400','2.400','1.600'],[10],['(4.00 − 1.60)/4.00','= 2.40/4.00 = 0.600.'],'kr-ratio',{'variance':4,'sumPQ':1.6})
calc('kr-result','For N = 10 items, SD² = 4.00, and Σpq = 1.60, what is KR-20? Round to two decimals.',
 '0.67',['0.60','0.40','1.11'],[10],['KR-20 = [10/9] × [(4.00−1.60)/4.00].','= 1.111111… × 0.600 = 0.666666…','Rounded to two decimals: 0.67.'],'kr20',{'n':10,'variance':4,'sumPQ':1.6},formula='KR-20 = [N/(N − 1)] × [1 − Σpq/SD²]')
calc('kr-calculate-q','For an item with p = 0.80, what is q? Round to two decimal places.',
 '0.20',['0.80','1.80','0.64'],[9],['q = 1 − p = 1 − 0.80 = 0.20.'],'q',{'p':0.8})
calc('kr-calculate-pq','For p = 0.80 and q = 0.20, what is pq? Round to two decimal places.',
 '0.16',['0.60','1.00','0.64'],[9],['pq = 0.80 × 0.20 = 0.16.'],'pq',{'p':0.8})
benchmarks=[('excellent','Excellent','r ≥ 0.90'),('good','Good','0.80 ≤ r < 0.90'),('acceptable','Acceptable','0.70 ≤ r < 0.80'),('questionable','Questionable','r < 0.70')]
for key,label,range_ in benchmarks:
 add('reliability','rating-'+key,f'According to the reliability deck, PDF page 11, which quality rating matches {range_}?',label,[r[1] for r in benchmarks if r[1]!=label],[11],
 'The slide\'s evaluation guide uses this rating. These thresholds are course guidelines; reliability requirements depend on the intended use and evidence.',source='reliability')
for key,prompt,ans,wrong in [
 ('excellent-use','Which use is associated with r ≥ 0.90 in the slide\'s guide?','High-stakes diagnostic decisions',['Tests automatically requiring item revision','Only informal formative checks','No assessment use at all']),
 ('good-use','Which use is associated with 0.80 ≤ r < 0.90?','Classroom grading and certification',['Only item revision','Only identifying sources','No grading decisions']),
 ('acceptable-use','Which use is associated with 0.70 ≤ r < 0.80?','Formative tests and research surveys',['Only high-stakes diagnostics','No research use at all','Automatic proof of validity']),
 ('low-use','What response does the slide recommend when r < 0.70?','Item revision or test lengthening',['Automatically treating it as excellent','Ignoring test quality entirely','Assuming perfect validity']),
]:add('reliability',key,'According to the evaluation guide on reliability PDF page 11, '+prompt[0].lower()+prompt[1:],ans,wrong,[11],
 f'The supplied benchmark table associates this range with {ans.lower()}. A reliability threshold alone does not establish suitability or validity.',source='reliability')
add('reliability','interpret-retest','What does the worked rₛ = 0.90 example indicate?', 'High temporal rank stability',
 ['No consistency of ranks','A proof of content validity','A negative relationship between forms'],[4],
 'Participants\' relative ranks are highly consistent across the two administrations.',source='reliability')
add('reliability','interpret-parallel','What does r = 0.93 indicate in the parallel-form example?', 'High equivalence of the two forms',
 ['Zero association between form scores','Automatic proof of predictive validity','A negative paired-score relationship'],[6],
 'The deck interprets the large positive paired-score correlation as high parallel-form equivalence.',source='reliability')
add('reliability','interpret-split','How does the worked correction change the reliability estimate?', 'From 0.70 for halves to about 0.82 for the whole test',
 ['From 0.82 to −0.70','From 0.70 to 1.40 as a reliability coefficient','From 0.70 to exactly 1.00'],[8],
 'The numerator 1.40 is not the coefficient; dividing by 1.70 gives approximately 0.82.',source='reliability')
add('reliability','interpret-kr','Under the slide\'s benchmark guide, how would the worked KR-20 value 0.67 be rated?',
 'Questionable',['Acceptable','Good','Excellent'],[10,11],
 '0.67 is below 0.70, the lower boundary of Acceptable in the supplied guide.',source='reliability')
add('reliability','summary','What does reliability estimation support in the final summary?', 'Fair, defensible assessment design',
 ['Automatic proof that all interpretations are valid','Eliminating the need to inspect items','Replacing all research evidence with one number'],[12],
 'The final slide connects reliability estimation with measurement precision and defensible assessment design.',source='reliability')

# Source inventory, per-page dispositions and traceable coverage.
def write_outputs():
    # Narrow grouped teaching references to the exact defining slide where needed.
    for q in QUESTIONS:
        key=q['id']
        if q['topic']=='instruments' and key.split('instruments-')[1] in {'validity','reliability','usability','content','concurrent','predictive','construct'}:
            q['sources']=[{'sourceId':'methods','pages':[28 if key=='instruments-reliability' else 29 if key=='instruments-usability' else 27]}]
        if key in {'frameworks-hypothesis','frameworks-null','frameworks-alternative','frameworks-assumption'}:
            q['sources']=[{'sourceId':'methods','pages':[45 if key=='frameworks-assumption' else 42]}]
        if key in {'historical-documents','historical-numbers','historical-oral','historical-relics'}:
            q['sources']=[{'sourceId':'methods','pages':[83 if key in {'historical-documents','historical-numbers'} else 84]}]
        if key.startswith('designs-') and key.removeprefix('designs-') in {r[0] for r in design_rows}:
            q['sources']=[{'sourceId':'methods','pages':[78 if key.removeprefix('designs-') in {'experiment','quasi','cross-correlation','expost'} else 79]}]
        if q['topic']=='variables' and key.removeprefix('variables-') in {'independent','dependent','intervening','control','moderator'}:
            q['sources']=[{'sourceId':'methods','pages':[23]}]
            if key in {'variables-independent','variables-dependent','variables-control'}:q['sources'][0]['pages'].append(74)
    for s in SOURCES:
        original=Path('C:/Users/Ivan/Downloads')/s['filename']
        s['sha256']=hashlib.sha256(original.read_bytes()).hexdigest()
    page_titles={
     'methods':{1:'Title',2:'Course description',3:'Course objectives',4:'Course content overview',5:'Introduction outline',6:'Problems and objectives outline',7:'Literature outline',8:'Designs outline',9:'Sampling outline',10:'Data collection outline',11:'Data processing outline',12:'Statistics outline',13:'Analysis and presentation outline',14:'Conclusions outline',15:'Proposal writing outline',16:'Course references',17:'Definitions of research',18:'Importance of research',19:'Characteristics of research',20:'Researcher mnemonic',21:'Classifications',22:'Variable definition',23:'Variable types',24:'Variable diagrams',25:'Numbered research process',26:'Detailed research process',27:'Validity types',28:'Reliability methods and malformed formulas',29:'Usability',30:'Lesson 2 title',31:'Research problem',32:'Repeated problem definition',33:'5W elements',34:'Problem characteristics',35:'Sources of problems',36:'Selection guidelines',37:'Formulating problems',38:'Title-writing tips',39:'Blank enrichment worksheet',40:'Blank enrichment worksheets',41:'Problems versus objectives',42:'Hypotheses',43:'Theoretical framework',44:'Conceptual framework',45:'Assumptions',46:'Significance',47:'Scope and limitations',48:'Definition types',49:'Repeated scope definition',50:'Lesson 3 title',51:'Related literature',52:'Review functions I',53:'Review functions II',54:'Review functions III',55:'Literature recency',56:'Literature characteristics',57:'Source categories',58:'Primary-source definition and overbroad examples',59:'Secondary-source definition and overbroad examples',60:'Where sources are located',61:'Related legal bases',62:'Historical nursing-law illustration',63:'Relevance and chronology',64:'Nursing-literature illustration',65:'Local and foreign studies',66:'Local-study illustration',67:'Conceptual definition',68:'Operational definitions',69:'Lesson 4 title',70:'Design definition',71:'Design meanings',72:'Parts of design',73:'Good-design considerations',74:'Important variables/concepts',75:'Experimental concepts',76:'Design categories and exploratory methods',77:'Formulative versus descriptive/diagnostic',78:'Design comparison table I',79:'Design comparison table II',80:'Historical section title',81:'Historical definition and limitations',82:'Historical uses',83:'Historical steps and written/numerical sources',84:'Oral/relic sources and evidence classification',85:'Primary/secondary examples',86:'Historical steps and external criticism',87:'External/internal criticism',88:'Descriptive section title',89:'Descriptive definitions',90:'Quantitative/qualitative description',91:'Descriptive values',92:'Descriptive types I',93:'Descriptive types II',94:'Comparative types/advantages/limits; mismatched paragraph',95:'Experimental section title',96:'Experimental definitions',97:'Distinguishing features',98:'Seven Ms',99:'Experimental plan and threats',100:'One-shot and one-group designs',101:'Static and randomized pretest-posttest',102:'Posttest-only control and Solomon four-group',103:'Nonequivalent/separate-sample text and inconsistent diagrams',104:'Time-series design'},
     'architecture':dict(enumerate(['Title','Method-action-output','Seven pillars','Professional and investigative purposes','Basic versus applied','Applied research and time dimensions','Methodological domains','Quantitative approaches','Quantitative classification and validity sidebar','Qualitative stages','Qualitative approaches','Mixed-method purposes','Infrastructure pyramid','Traditional versus e-Research','Ecosystem flow'],1)),
     'reliability':dict(enumerate(['Title','Four reliability methods','Test-retest formula','Spearman rank example','Parallel-forms formula','Pearson example','Split-half formula','Spearman-Brown example','KR-20 formula','KR-20 example','Benchmarks','Summary'],1))}
    supporting={'methods':{1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,30,50,69,80,88,95},'architecture':{1},'reliability':{1}}
    repeated={'methods':{32,49},'architecture':set(),'reliability':set()}
    exceptions=[
      {'sourceId':'methods','pages':list(range(5,16)),'reason':'Outline-only topics are contextual labels; no unsupported detailed sampling/statistics/proposal questions are invented.'},
      {'sourceId':'methods','pages':[39,40],'reason':'Blank enrichment forms require personal/student input; no fixed answer key is supplied.'},
      {'sourceId':'methods','pages':[28],'reason':'Malformed formula glyphs are not scored as exact mathematics. The separate reliability deck supplies readable formulas; the split-half administration contradiction is explicitly tested with a clarification.'},
      {'sourceId':'methods','pages':[94],'reason':'The genetic-method paragraph conflicts with its heading. A source-specific heading question and comparison note cover it without inventing a reconciled definition.'},
      {'sourceId':'methods','pages':[103],'reason':'Exact reconstruction of the ambiguous separate-sample X layout is excluded; readable prose is tested. The extra X in the nonequivalent control row is explicitly identified and a corrected schematic is labeled.'},
    ]
    inventory=[]
    for s in SOURCES:
      for n in range(1,s['pages']+1):
       ids=[q['id'] for q in QUESTIONS if any(r['sourceId']==s['id'] and n in r['pages'] for r in q['sources'])]
       status='repeated' if n in repeated[s['id']] else 'covered' if ids else 'supporting material' if n in supporting[s['id']] else 'excluded'
       reason='Question IDs below cover the substantive teaching content.' if status=='covered' else 'Repeated teaching content links to the same questions.' if status=='repeated' else 'Title, course context, outline, or reference material; no substantive standalone assessment invented.' if status=='supporting material' else 'Blank personal-response activity; no fixed source-supported answer.'
       inventory.append({'sourceId':s['id'],'page':n,'title':page_titles[s['id']][n],'status':status,'reason':reason,'questionIds':ids})
    bank={'version':1,'title':'Fundamentals of Research Exam Reviewer','sources':SOURCES,
          'topics':[{'id':id,'title':title,'description':desc} for id,title,desc in TOPICS], 'questions':QUESTIONS}
    # Structural content version: saved answers are additionally guarded per question.
    bank['contentVersion']=hashlib.sha256(json.dumps(QUESTIONS,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:16]
    for folder in ['data','audit']:(ROOT/folder).mkdir(exist_ok=True)
    def save(path,value): (ROOT/path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    save('data/questions.json',bank)
    (ROOT/'data/bank.js').write_text('window.RESEARCH_BANK = '+json.dumps(bank,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    save('audit/source-inventory.json',{'sources':SOURCES,'pages':inventory,'exceptions':exceptions,'reviewMethod':'Text extraction plus visual inspection of all 75 image-based pages and formula/diagram close-ups. Source text is paraphrased into authored questions; diagrams are transcribed and labeled.'})
    lines=['# Source coverage','',f'{len(QUESTIONS)} authored multiple-choice questions across {len(TOPICS)} topics; all 131 PDF pages inventoried.','',
      'Coverage is a human-authored content review, separate from the automated application tests. All source IDs use PDF page numbers, not printed slide numbers.','',
      '## Topic counts','', '| Topic | Questions |','|---|---:|']
    lines += [f'| {title} | {sum(q["topic"]==id for q in QUESTIONS)} |' for id,title,_ in TOPICS]
    lines += ['','## Coverage exceptions','']+[f'- {e["sourceId"]}, PDF pages {", ".join(map(str,e["pages"]))}: {e["reason"]}' for e in exceptions]
    lines += ['','## Page inventory','', '| Source | PDF page | Content | Disposition | Question IDs |','|---|---:|---|---|---|']
    lines += [f'| {p["sourceId"]} | {p["page"]} | {p["title"]} | {p["status"]} | '+', '.join(p['questionIds'])+' |' for p in inventory]
    lines += ['','## Clarifications','']
    for q in QUESTIONS:
      if q.get('clarification'):
       lines += [f'### {q["id"]}',q['prompt'],'',q['clarification']['text'],'',*[f'- [{r["title"]}]({r["url"]})' for r in q['clarification']['references']],'']
    (ROOT/'audit/COVERAGE.md').write_text('\n'.join(lines).rstrip()+'\n',encoding='utf-8')
    print(f'Authored {len(QUESTIONS)} questions; {len(inventory)} source pages; {sum(bool(q.get("clarification")) for q in QUESTIONS)} clarifications.')

if __name__=='__main__':write_outputs()
