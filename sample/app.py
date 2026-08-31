"""Tiny starter for Dev UI doc screenshots. Two Gemini models, three menu flows.

Do not replace this with VertexAI() or GoogleAI() as a plugin — those list a catalog
and the home shot stops looking like something you just started.
"""

from genkit import Genkit
from genkit.model import model_action_metadata
from genkit_google_genai import VertexAI
from genkit_google_genai.google import vertexai_name
from genkit_google_genai.models.gemini import get_model_config_schema, google_model_info
from pydantic import BaseModel

_MODELS = ('gemini-2.5-flash', 'gemini-2.5-pro')


class TinyVertex(VertexAI):
    """Only the two models a starter would show. No catalog, no evaluators."""

    async def init(self):
        return [a for n in _MODELS if (a := self._resolve_model(vertexai_name(n)))]

    async def list_actions(self):
        return [
            model_action_metadata(
                name=vertexai_name(n),
                info=google_model_info(n).model_dump(by_alias=True),
                config_schema=get_model_config_schema(n),
            )
            for n in _MODELS
        ]


ai = Genkit(
    plugins=[TinyVertex(project='aim-testing', location='us-central1')],
    model=VertexAI.gemini_model('gemini-2.5-flash'),
)


class ThemeInput(BaseModel):
    theme: str = 'medieval'


class MenuSuggestion(BaseModel):
    starter: str
    soup: str
    main: str
    dessert: str


class MenuQuestion(BaseModel):
    question: str = 'What is a good starter for two people?'


class MenuAnswer(BaseModel):
    answer: str


ai.define_prompt(name='hello', prompt='Write a one-line greeting for a restaurant host.')


@ai.flow()
async def menuSuggestionFlow(theme_input: ThemeInput) -> str:
    result = await ai.generate(
        prompt=f'Invent one {theme_input.theme}-themed restaurant dish. One sentence.',
    )
    return result.text


@ai.flow()
async def complexMenuSuggestionFlow(theme_input: ThemeInput) -> MenuSuggestion:
    await ai.generate(prompt='What makes a good prix fixe menu? Answer in two sentences.')
    await ai.generate(
        prompt=(
            'What ingredients, seasonings, and cooking techniques would work '
            f'for a {theme_input.theme} themed menu? Keep it short.'
        )
    )
    result = await ai.generate(
        prompt=(
            f'Invent a prix fixe menu for a {theme_input.theme} themed restaurant. '
            'Return starter, soup, main, and dessert.'
        ),
        output_schema=MenuSuggestion,
    )
    if result.output is None:
        raise RuntimeError('No menu generated')
    return result.output


@ai.flow()
async def menuQuestionFlow(question_input: MenuQuestion) -> MenuAnswer:
    async def retrieve_daily_menu() -> str:
        return (
            'Starter: roasted beet salad with goat cheese.\n'
            'Soup: roasted tomato basil.\n'
            'Main: herb-crusted salmon, lemon butter.\n'
            'Dessert: dark chocolate tart.'
        )

    menu = await ai.run(name='retrieve-daily-menu', fn=retrieve_daily_menu)
    result = await ai.generate(
        system="Help the user answer questions about today's menu.",
        prompt=f"Today's menu:\n{menu}\n\nQuestion:\n{question_input.question}",
    )
    return MenuAnswer(answer=result.text)


async def main() -> None:
    return None


if __name__ == '__main__':
    ai.run_main(main())
