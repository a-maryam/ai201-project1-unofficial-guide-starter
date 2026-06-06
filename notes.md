First prompt

Can you use planning.md as a basis to write a script to load all the documents from docs, define a method for paragraph chunking, define a method for fixed-length chunking as per parameters in planning.md? Do the previous as functions, then make the appropriate calls to paragraph chunk and fixed-length chunk respectively as define.

Chunks:

Total chunks: 369

# Notes about reddit chunks
    Seems like there are a lot of things semantically mixed together in the reddit chunks that I printed...hopefully the paragraph split is better.

{'source': '10_reddit_cs_2.txt', 'method': 'fixed', 'chunk_index': 0, 'text': "How is the Computer Science and Math departments here?\nAre the professors good? I've heard a lot about them.\nAlone-Monk\n•\n1y ago\nI dunno much about comp sci but our Math department is really good imo\n\n\nUpvote\n4\n\nDownvote\n\nReply\n\nAheniru\n•\n1y ago\nAlum (class of '24)\nI’ve heard the math department is one of the best and CS is not the best but depends. I was a CS major (‘24) - I think BMC generally had better intro CS classes. I think ML and data science at Hav was absolutely fantastic due to the p"}


{'source': '10_reddit_cs_2.txt', 'method': 'fixed', 'chunk_index': 1, 'text': "ad better intro CS classes. I think ML and data science at Hav was absolutely fantastic due to the profs teaching it while I was there. I think it was better there than at Penn. I also appreciate how there’s not a weeding out process in CS in the bi-co but I definitely feel like the intro classes are the hardest and it gets easier from there.\n\n\n\nUpvote\n3\n\nDownvote\n\nReply\n\nseaflans\n•\n1y ago\nThe hardest is definitely Dianna Xu's Analysis of Algorithms at BMC, but it's also a great class. I think i"}


{'source': '10_reddit_cs_2.txt', 'method': 'fixed', 'chunk_index': 2, 'text': "dest is definitely Dianna Xu's Analysis of Algorithms at BMC, but it's also a great class. I think it's listed as CS340.\n\n\n\nUpvote\n2\n\nDownvote\n\nReply\n\nAheniru\n•\n1y ago\nAlum (class of '24)\nI took it with Lindell since I was not confident with being able to pass her class haha Her OS class is also very hard (I’ve heard)\n\n\n\nUpvote\n2\n\nDownvote\n\nReply\n\nseaflans\n•\n1y ago\nPretty sure analysis of algorithms with Dianna was my worst grade on my transcript, and I was quite pleased with the grade I receive"}


{'source': '10_reddit_cs_2.txt', 'method': 'fixed', 'chunk_index': 3, 'text': "ms with Dianna was my worst grade on my transcript, and I was quite pleased with the grade I received.\n\n\nUpvote\n2\n\nDownvote\n\nReply\n\nu/Kingtastic1 avatar\nKingtastic1\n•\n1y ago\nJunior (class of '28)\nThe computer science department is hit or miss. I've known two professors that are leaving after this year, and I also know students that came in being a compsci major and completely switching out because they felt like the department isn't helping them learn how to program. I've personally found it oka"}


{'source': '10_reddit_cs_2.txt', 'method': 'fixed', 'chunk_index': 4, 'text': "they felt like the department isn't helping them learn how to program. I've personally found it okay, but it is the courses I am performing the worst in academically (I am a CS major)\n\n\n\nUpvote\n2\n\nDownvote\n\nReply\n\nAheniru\n•\n1y ago\nAlum (class of '24)\nWhich profs are leaving?\n\n\n\nUpvote\n1\n\nDownvote\n\nReply\n\nu/Kingtastic1 avatar\nKingtastic1\n•\n1y ago\nJunior (class of '28)\nI'll PM you.\n\n\nUpvote\n2\n\nDownvote\n\nReply\n\nDifferentSea5841\n•\n1y ago\nWhich professors are leaving?\n\n\nUpvote\n1\n\nDownvote\n\nReply\n\nCi"}


# Lottery info chunks:
    The preamble type paragraphs don't seem to be helpful. But I think the course info is chunked together

{'source': '11_haverford_cs_reqs.txt', 'method': 'paragraph', 'chunk_index': 32, 'text': 'In addition to submitting the written thesis document, students must also complete the assigned presentation elements, which typically include a December poster presentation of the thesis topic and scope, and the final oral presentation of the thesis. These presentations are graded on evidence of preparation and on participation (i.e. showing up on time for one’s own presentation, attending the rehearsals of a few others, and providing feedback and/or asking questions). Faculty will provide info'}


{'source': '11_haverford_cs_reqs.txt', 'method': 'paragraph', 'chunk_index': 33, 'text': 'hearsals of a few others, and providing feedback and/or asking questions). Faculty will provide informal feedback to the presenters on speaking style, professionalism, diction/grammar, poise, etc., but these elements are not included in the grade.'}


{'source': '11_haverford_cs_reqs.txt', 'method': 'paragraph', 'chunk_index': 34, 'text': 'Minor Requirements\nThe Computer Science minor requirements follow the same philosophy and structure as the major:'}


{'source': '11_haverford_cs_reqs.txt', 'method': 'paragraph', 'chunk_index': 35, 'text': 'the introductory sequence\nbreadth: a 200-level course in each element of the field (theory, systems, and applications)\ndepth: one year-long sequence (200-level into 300-level) in either theory, systems, or applications\nCMSC H105 Introduction to Computer Science or CMSC H107 or Bryn Mawr CMSC B113.\nCMSC H106 Introduction to Data Structures or CMSC H107 or Bryn Mawr CMSC B151.\nCMSC H231 Discrete Mathematics\nStudents with strong backgrounds in mathematics and prior knowledge of the topics covered i'}


{'source': '11_haverford_cs_reqs.txt', 'method': 'paragraph', 'chunk_index': 36, 'text': 'hematics\nStudents with strong backgrounds in mathematics and prior knowledge of the topics covered in CMSC H231 may wish to seek instructor permission to place into CMSC H340 /CMSC H345 without prior completion of CMSC H231—in this case, the student may complete the requirements for the minor with another course covering discrete mathematics, from the following list: MATH H210 (Linear Optimization), MATH H394 (Logic), MATH H394 (Cryptography), MATH H395 (Combinatorics), or STAT H203, STAT H218,'}


{'source': '11_haverford_cs_reqs.txt', 'method': 'paragraph', 'chunk_index': 37, 'text': '), MATH H394 (Logic), MATH H394 (Cryptography), MATH H395 (Combinatorics), or STAT H203, STAT H218, STAT H286, or STAT H396.\nCMSC H251 Principles of Computing Systems\nStudents wishing to continue to CMSC B355 may substitute CMSC B223 Systems Programming\nStudents not taking a 35X course may substitute CMSC H240 Principles of Computer Organization or CMSC H245 Principles of Programming Languages\nCMSC H260 Foundations of Data Science\nOne 300-level core course from the following list\nCMSC H340 Analy'}

------------------------------------------------

Retrieval of chunks

1. What is CS240 about? — ⚠️ Can't answer. As we discussed, retrieval returned other catalog entries (H245, H251, H260) and no description of H240 exists in the documents. The corpus only knows H240's title ("Principles of Computer Organization") from the requirements page. This is your failure case.

2. What is Professor Wonacott like? — ✅ Strong, and matches your expected answer. The RMP reviews are genuinely mixed: praised as friendly, caring, passionate, knowledgeable, a good/clear grader ("really an amazing professor," "AWESOMMMME"), but repeatedly criticized as long-winded — "over-explains," "windbag," "takes an hour and a half to explain something that could've been covered in 5 minutes," talks too fast. Several reviewers recommend knowing Python beforehand. That's almost exactly your planning.md expected answer ("friendly, not the best at teaching, long-winded").

3. What is the course lottery like at Haverford? — ✅ Accurate but procedural. Retrieval pulled the official lottery guidelines: you must register by the deadline to be entered; the Registrar runs the lottery right after; you can request preferential treatment if you've been lotteried out before; first-years get reserved spots in lower-division courses; upper-division goes by seniority. Note: this is the official mechanics, not the student-stress angle your expected answer described ("stressful, not guaranteed, usually ok"). The "brutal lottery" sentiment actually lives in 2_college_confidential.txt, which ranked #5 — so retrieval leaned official over informal here.

4. What is the CS department like? — ✅ Matches well. Sources converge on: more theoretical than applied, smaller but growing, supportive professors but hit-or-miss overall, with the faculty-shortage article adding context about strain. College Confidential: "more of a theoretical background… not one of the larger ones… very challenging but professors are very supportive." Lines up with your expected answer ("nice, theoretical over applied").

5. What courses should a first-year take, and are they difficult? — ⚠️ Partial. Retrieval got the sentiment — intro courses are "rigorous but not unmanageable," people were "fond of both the regular and accelerated intro courses," and the intro classes are "the hardest, it gets easier from there." But it did not cleanly surface the specific CS105-vs-CS106 placement guidance from your expected answer. That detail lives in the requirements file, which didn't rank in the top 5 — a retrieval gap worth noting.

Summary: 2 strong (Wonacott, department), 2 partial (lottery leans official; first-year missing the 105/106 specifics), 1 fail (CS240, corpus gap). That's a solid, honest basis for your Evaluation Report table — and questions 3 and 5 give you a second failure-mode to discuss: the right chunk existed but ranked just outside top-k. Bumping k to 7–8, as you anticipated in planning.md, might recover both.


#	Question	Best dist	Top-5 spread	Read
1	CS240	0.549	0.549 → 0.599	⚠️ weak & flat
2	Wonacott	0.433	0.433 → 0.577	✅ strong
3	Lottery	0.330	0.330 → 0.519	✅ very strong
4	CS dept	0.431	0.431 → 0.526	✅ strong
5	First-year	0.361	0.361 → 0.465	✅ strong