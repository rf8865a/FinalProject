# FinalProject
Rachel Freedman 

This is my final project. After working this past summer at an estate planning firm I realized there were a lot of mispelling of names and incorrect dates on the documents. Command F did not work well for mispelled names because they would not come up when searching with the correct spelling. The dates would be incorrect when meetings would be pushed back and the documents would not get updated. Names that had more than one way to be spelled or were complicated to spell would also go un noticed at times. I used the read, list, and write tool schemas to read the documents I uploaded for incorrect spelling and dates, list all the files and then write a new document with the correct spelling and dates. 

For this code to work the document you want the AI agent to check has to be listed on line 80. For example if I want it to correct will1.txt I need to input that. The correct spelling and dates for each document are in correctcontents.txt. 

At first I had a seperate code for each the spelling and the dates. I also had too much information in the content section of the code and it was not efficient. In order to make the code more efficient I combined the spelling and date check into fix_content and check_content rather than having a seperate check_spelling and check_date. Now all I have to do is change the document I want checked and fixed rather than give the AI the correct spelling and name of a new document each time. 

A major error I ran into when making this change was that the document AI was giving back would just have the correct name and correct date without the rest of the content. While that is helpful, I wanted the document revised. When i added the word "throughout" to the content section this seemed to fix the issue and the AI was giving a fully corrected version of the original document. 


