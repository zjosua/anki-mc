## Config Options

- `answerColoring` (`string`)
    - `DEFAULT_COLORING` (default): If a row was ticked or left unticked correctly it is shown green and red otherwise.
    - `ALTERNATE_COLORING`: Only color falsely ticked rows red and rows that should have been ticked green.
- `colorQuestionTable` (`bool`)
    - `true`: Color the table with your chosen answers according to their correctness.
    - `false` (default): Don't modify the table with your chosen answers.
- `colorAnswerTable` (`bool`)
    - `true` (default): Color the table with the correct answers according to your chosen answers.
    - `false`: Don't modify the table with the correct answers.
- `hideAnswerTable` (`bool`)
    - `true`: Only show the table with your chosen answers.
    - `false` (default): Show the table with the correct answers after confirming your chosen answers.
- `maxQuestions` (`number`)
    - `n`: The number of questions that may be filled with options is `n` (default is `5`)
- `maxQuestionsToShow` (`number`)
    - `0`: (default) Show all questions that are defined in the fields on the card
    - `n >= 1`: Show only `n` questions from the ones defined in the fields on the card
