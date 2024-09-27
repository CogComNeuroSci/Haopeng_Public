var informed_consent = {
    type: jsPsychHtmlButtonResponse,
    stimulus: `
        <p>Please only participant in this study in case you have no knowledge about Swahili.</p> 
        <p>Please scroll to read the information and terms below, and click the correct button at the end of this page.</p><br><br>
        <div style="width:${1/2*screen.width}px; height:${1/2*screen.height}px; overflow-y:scroll; font-size:10px; border-style: solid; border-color: black; border-width: 1px; text-align:left">
            <p style="font-weight:bold; font-size:25px; text-align:center">Information letter and consent form</p>

            <p style="font-weight:bold; font-size:20px; text-align:center">Part 1: Information Letter</p>

            <p style="font-weight:bold; font-size:15px">A. Information about the study</p>
            <p>Dear,<br>
                You are invited to participate in this online study from Ghent University. Please take enough time to read this information letter carefully before you decide to participate in this study. Do not hesitate to ask questions to the researcher if there are any confusion or if you would like additional information. Because this is an online study, you can only send messages to researchers through Prolific. Make sure you understand everything. Once you have decided to participate in the study, you will be asked to sign the consent form at the end (click a specific button in the online study).</p>
            
            <p style="font-weight:bold; font-size:10px">What is the purpose of the research?</p>
            <p>The primary goal of this study is to explore the cognitive processes involved in learning a new language. Specifically, you will learn a series of English-Swahili word pairs. The study is divided into two main parts. In the first part, you will get familiar with 90 English-Swahili word pairs (Phase 1) and complete two practice tests (Phases 2 and 3). In the second part, you will take two final tests to assess your learning performance (Phases 4 and 5).</p>
            
            <p style="font-weight:bold; font-size:10px">Ethical approval</p>
            <p>The study is conducted according to the guidelines set out in the General Ethical Protocol of the Faculty of Psychology and Educational Sciences (Ghent University). The researchers conduct this study in accordance with accepted standards of scientific and ethical conduct. In doing so, they apply good research practices and adhere to the principles of research ethics as described in "Ethics in Social Science and Humanities" (EU, 2018).</p>
            
            <p style="font-weight:bold; font-size:15px">B. Information regarding participation</p>

            <p style="font-weight:bold; font-size:10px">What does taking part in this study involve?</p>
            <p>This study will last about 80 minutes. You need to use your mouse and keyboard to interact with this online experiment. In part 1, you need to learn 90 English-Swahili word pairs and have two practical tests. In part 2, you need to complete two final tests to check your learning performance.<br>
            Participation in this study is completely voluntary and there can be no coercion in any way. You may refuse to participate in the study and you may withdraw from the study at any time without having to give a reason. If you refuse to participate, or if you decide to withdraw from an ongoing study, this will in no way affect your continued relationship with the researcher, your evaluation and/or study supervision (if you are a student) or your treatment (if you have a therapeutic relationship with the researcher).<br>
            If you wish, you can get a summary of the study findings after the study is completed and the results are known. To get a summary, you can request this from the researcher you are in contact with (though Prolific). 
            </p>

            <p style="font-weight:bold; font-size:10px">What are the risks and benefits of participating in this study?</p>
            <p>There is no known permanent risk associated with this study.</p>

            <p style="font-weight:bold; font-size:10px">Is any compensation or reward provided for participation in this study?</p>
            <p>The payment for this study is £12 and will be paid through Prolific.</p>

            <p style="font-weight:bold; font-size:15px">C. Information on Privacy and Personal Data</p>
            <p>The legal framework for the processing of personal data and confidential information in the context of this study is determined by:<br>
                The European General Data Protection Regulation 2016/679 of 27 April 2016, effective since 25 May 2018 (this is the AVG or GDPR);<br>
                The Belgian Law on the Protection of Natural Persons with regard to the Processing of Personal Data of 30 July 2018<br>
            Researchers must comply with the Ghent University generic code of conduct for processing personal data.
            </p>

            <p style="font-weight:bold; font-size:10px">What personal data are collected?</p>
            <p>The following personal data will be processed: Age, gender, accuracy and response times to computer tasks.<br>
                Personal data will be collected from Prolific or using computer tasks.
            </p>

            <p style="font-weight:bold; font-size:10px">Why are these personal data collected?</p>
            <p>We need to report the gender and age distribution when publishing the paper. The accuracy and response times will be used for the formal analysis.</p>

            <p style="font-weight:bold; font-size:10px">On what legal ground will the data be processed?</p>
            <p>To process your personal data, your explicit consent will be sought. This is done by signing a 'consent form'. This consent can be withdrawn at all times by notifying the principal investigator.</p>

            <p style="font-weight:bold; font-size:10px">Who has access to my (personal) data?</p>
            <p>The researchers at Ghent University have access to the data for analysis and replication of our statistical results. All the data will be anonymized.<br>
            The researchers outside Ghent University have access to the data to replicate our statistical results. All the data will be anonymized.
            </p>

            <p style="font-weight:bold; font-size:10px">Reuse of data</p>
            <p>The research data collected here may also still be useful in answering other research questions. Therefore, the possibility exists that the research data may be reused at a later date for another research. The reuse of the research data can be done both within the own research team and by external researchers within and outside the European Union. To this end, research data will be made available in a controlled manner via a dedicated research data sharing platform. In doing so, all necessary measures will be taken to guarantee the confidentiality of your personal data as prescribed in the Ghent University Generic Code of Conduct for handling personal data and confidential information.</p>

            <p style="font-weight:bold; font-size:10px">What rights do you have as a participant regarding your personal data?</p>
            <p>In accordance with European and Belgian privacy legislation, your privacy is respected. As already indicated, you can withdraw your consent at any given moment and without giving any reason. This means that your data will not be further processed from the moment of withdrawal.<br>
            You have the right to inspect the data collected about you and you may also request a copy, provided this does not infringe the rights and freedoms of others, including those of Ghent University. Any inaccurate data about you can be corrected at your request. Furthermore, you have the right to be forgotten. This means that, after withdrawing your consent, you may ask for your personal data to be deleted.<br>
            To exercise any of the above rights, please contact the researchers through Prolific.
            </p>

            <p style="font-weight:bold; font-size:10px">If you have a complaint</p>
            <p>If you would like to file a complaint about the way your personal data is handled or if you have any questions regarding your personal data in the context of this study, you may contact Ghent University's Data Protection Officer at privacy@ugent.be or T 09 264 95 17.<br>
            You may also file a complaint with the Data Protection Authority, Drukpersstraat 35, 1000 Brussels (e-mail: contact@apd-gba.be) and/or the Vlaamse Toezichtcommissie (e-mail: contact@toezichtscommissie.be). 
            </p>

            <p style="font-weight:bold; font-size:20px; text-align:center">Part 2: Consent Form</p>
            <p style="font-weight:bold; font-size:15px">A. Consent regarding participation in the study</p>
            <p>I voluntarily participate in this scientific study.</p>
            <p>I know that I may withdraw from the study at any time without giving a reason for this decision and that this will not in any way affect my further relationship with the researcher.<br>
            If I am participating as part of my training, I understand that early termination of my participation will not adversely affect my evaluation and/or study supervision.<br>
            I understand that discontinuing my participation will not negatively affect my treatment or support.<br>
            </p>
            <p>I have read the information form and received sufficient explanation about the nature, purpose, duration, and anticipated effects of the study. I was given the opportunity to ask questions and I received satisfactory answers to all my questions.</p>
            <p>There is no known permanent risk associated with this study.</p>

            <p style="font-weight:bold; font-size:15px">B. Consent regarding the processing of personal data</p>
            <p>I know that I have rights to safeguard my privacy (including access, correction, deletion) and to whom I should turn to exercise these rights.</p>
            <p>I give permission to the researchers to collect, process, store, analyse and report on my (personal) data for the purposes of this study.</p>
            <p>I consent to be recognisably included in publications as part of this study.</p>

            <p style="font-weight:bold; font-size:15px">C. Consent regarding re-use and sharing of data</p>
            <p>I give permission to researchers of the research group to reuse my data for further similar scientific research.</p>
            <p>I give permission to the researchers to share my data for further similar scientific research and this within and outside the European Economic Area. In doing so, all necessary measures will be taken to protect the confidentiality of my personal data.</p>

        </div><br><br>
    `,
    choices: ['Yes', 'No'],
    prompt: '<p>Do you agree with all the terms in the consent form and want to continue?</p>',
    data: {useful_data: false},
    on_finish: function (data) {
        if (data.response == 1) {
            jsPsych.endExperiment('As you have indicated that you do not consent to participate in this study, please return this submission on Prolific by selecting the "stop without completing" button');
            completion_code = "location.href = 'https://app.prolific.com/submissions/complete?cc=C1KZ25MY'";
        }
    }
}