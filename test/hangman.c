#include <stdio.h>

void print_gallow(int i) {
	printf("Amount of wrong letters: %d\n\n", i);
	if (i == 0)
	{
		printf("\n");
		printf("\n");
		printf("\n");
		printf("\n");
		printf("\n");
		printf("\n");
		printf("____________\n\n");
		return;
	}

	if (i == 1)
	{
		printf("\n");
		printf("  |\n");
		printf("  |\n");
		printf("  |\n");
		printf("  |\n");
		printf("  |\n");
		printf("__|_________\n\n");
		return;
	}

	if (i == 2)
	{
		printf("  _______\n");
		printf("  |\n");
		printf("  |\n");
		printf("  |\n");
		printf("  |\n");
		printf("  |\n");
		printf("__|_________\n\n");
		return;
	}

	if (i == 3)
	{
		printf("  _______\n");
		printf("  |/\n");
		printf("  |\n");
		printf("  |\n");
		printf("  |\n");
		printf("  |\n");
		printf("__|_________\n\n");
		return;
	}

	if (i == 4)
	{
		printf("  _______\n");
		printf("  |/   | \n");
		printf("  |    O \n");
		printf("  |\n");
		printf("  |\n");
		printf("  |\n");
		printf("__|_________\n\n");
		return;
	}

	if (i == 5)
	{
		printf("  _______\n");
		printf("  |/   | \n");
		printf("  |    O \n");
		printf("  |    |\n");
		printf("  |    |\n");
		printf("  |\n");
		printf("__|_________\n\n");
		return;
	}

	if (i == 6)
	{
		printf("  _______\n");
		printf("  |/   | \n");
		printf("  |    O \n");
		printf("  |   \\|\n");
		printf("  |    | \n");
		printf("  |\n");
		printf("__|_________\n\n");
		return;
	}

	if (i == 7)
	{
		printf("  _______\n");
		printf("  |/   | \n");
		printf("  |    O \n");
		printf("  |   \\|/\n");
		printf("  |    | \n");
		printf("  |\n");
		printf("__|_________\n\n");
		return;
	}

	if (i == 8)
	{
		printf("  _______\n");
		printf("  |/   | \n");
		printf("  |    O \n");
		printf("  |   \\|/\n");
		printf("  |    | \n");
		printf("  |   /\n");
		printf("__|_________\n\n");
		return;
	}

	if (i == 9)
	{
		printf("  _______\n");
		printf("  |/   | \n");
		printf("  |    O \n");
		printf("  |   \\|/\n");
		printf("  |    | \n");
		printf("  |   / \\\n");
		printf("__|_________\n\n");
		return;
	}

	if (i == 10)
	{
		printf("  _______\n");
		printf("  |/   | \n");
		printf("  |    X \n");
		printf("  |   \\|/\n");
		printf("  |    | \n");
		printf("  |   / \\\n");
		printf("__|_________\n\n");
		return;
	}
}

int strlen2(char s[])
{
	int i = 0;
	while (s[i] != 0)
	{
		i = i+1;
	}

	return i;
}

int strcmpSpecial(char s1[], char s2[])
{
	int i = 0;
	int lengthS1 = strlen2(s1);
	int lengthS2 = strlen2(s2);

	while(i < lengthS1 && i < lengthS2)
	{
		if (s1[i] == 0)
			return 1;
		if(s1[i] != s2[i])
			return 0;
		i = i + 1;
	}

	return 1;
}

int main()
{
	char words[] = " strengths gypsy rhythmic cognac jukebox taxicab sprightly asthma orphan months depths geniuses withhold powwow myths bookkeeper stretchmarks kamikaze ombudsman quagmire mannequin caribou nymph skiing queueing symphony crypt wintry uncopyrightable twelfth sequoia gauntlet zoology unscrupulous parcheesi furlough coffee papaya hitchhiker catchphrase paprika savvy impromptu knickknack cyclists daydreamt plateaued cushion alfalfa jambalaya karaoke anchovy borscht messiah cockatoo rendezvous marriage children summer contest ";
	int numberWord = -1;
	int tmp = 1;
	int tmp2 = 0;
	int begin = 0;
	int end = 0;
	int lengthWord;
	char word[10]; 
	char guess[10]; 
	int error = 0;
	int userWon = 0;
	char inputLetter; 
	printf(" _     _                                     \n");
	printf("(_)   (_)                                    \n");
	printf(" _______ _____ ____   ____ ____  _____ ____  \n");
	printf("|  ___  (____ |  _ \\ / _  |    \\(____ |  _ \\ \n");
	printf("| |   | / ___ | | | ( (_| | | | / ___ | | | |\n");
	printf("|_|   |_\\_____|_| |_|\\___ |_|_|_\\_____|_| |_|\n");
	printf("                    (_____|                  \n");
	printf("Hangman Rules:\n");
	printf(" Only lowercase letters are allowed \n");
	printf(" You can only make 10 mistakes, while guessing the letter, otherwise it is game over\n");
	while (numberWord < 1 || numberWord > 60)
	{
		printf("Pick a number from 1 to 60: ");
		scanf("%d", &numberWord);
	}

	while (tmp < numberWord+1)
	{
		if (words[tmp2] == ' ' && tmp2 != 0)
		{
			tmp = tmp+1;
			if (begin != 0)
			{
				end = tmp2-1;
			}
		}
		tmp2 = tmp2 + 1;
		if (tmp == numberWord && begin == 0)
		{
			begin = tmp2;
		}
	}
	tmp = 0;
	while (begin+tmp < end+2)
	{
		word[tmp] = words[begin+tmp];
		tmp = tmp + 1;
	}
	lengthWord = end-begin+1;
	printf("The word size equals %d \n\n\n", lengthWord );
	printf("You can now start the game by guessing the first letter: \n");

	tmp = 0;
	while (tmp < lengthWord)
	{
		guess[tmp] = '.';
		tmp = tmp + 1;
	}
	guess[lengthWord] = (char)0;
	word[lengthWord]  = (char)0;
	while (error < 11 && !userWon)
	{
		int guessedLetter = 0;
		scanf("%c", &inputLetter);
		if (inputLetter != '\n')
		{
			if (isdigit(inputLetter))
			{
				printf("Impermissible character, try again\n");
				continue;
			}
			tmp = 0;
			while (tmp < lengthWord)
			{
				if (word[tmp] == inputLetter)
				{
					guess[tmp] = inputLetter;
					guessedLetter = 1;
				}
				tmp = tmp + 1;
			}
			if (!guessedLetter )
			{
				printf("%c is wrong \n\n\n", inputLetter);
				error = error + 1;
			}
			else
			{
				printf("%c is right \n\n\n", inputLetter);
			}
			printf("Your guess: %s \n", guess);
			print_gallow(error);
			printf("\n\n\n", guess);
			if (strcmpSpecial(guess, word))
			{
				userWon = 1;
				printf("Congratulations, you won (the word was %s)\n", guess);
			}
			if (error == 10)
			{
				printf("Game over! (the word was %s)\n", word);
				return 0;
			}
		}
	}
	return 0;
}
