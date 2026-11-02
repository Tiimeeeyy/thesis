---
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- dense
- generated_from_trainer
- dataset_size:66220
- loss:MultipleNegativesRankingLoss
- loss:CoSENTLoss
base_model: microsoft/unixcoder-base
widget:
- source_sentence: '[CARD] Ally of Justice Light Gazer

    [STATS] Level 8 ATK 2400 DEF 1600 Race 32 Attr 32

    [PSCT] 1 Tuner + 1 or more non-Tuner monsters

    This card gains 200 ATK for each LIGHT monster in your opponent''s Graveyard.

    [LUA]

    Synchro.AddProcedure(c,nil,1,1,Synchro.NonTuner(nil),1,99)

    [EFFECT 1]

    TYPE: EFFECT_TYPE_SINGLE | CAT: NONE

    CODE: EFFECT_UPDATE_ATTACK | PROP: EFFECT_FLAG_SINGLE_RANGE

    RANGE: LOCATION_MZONE | LIMIT: NONE

    FLOW: PASSIVE'
  sentences:
  - "[CARD] Lunalight Black Sheep\n[STATS] Level 2 ATK 100 DEF 600 Race 32768 Attr\
    \ 32\n[PSCT] You can discard this card, then activate 1 of these effects;\r\n\
    ● Add 1 \"Lunalight\" monster from your Graveyard to your hand, except \"Lunalight\
    \ Black Sheep\".\r\n● Add 1 \"Polymerization\" from your Deck to your hand.\r\n\
    If this card is sent to the Graveyard as a Fusion Material for a Fusion Summon:\
    \ You can add to your hand, 1 face-up \"Lunalight\" Pendulum Monster from your\
    \ Extra Deck or 1 \"Lunalight\" monster from your Graveyard, except \"Lunalight\
    \ Black Sheep\".\n[LUA]\n[EFFECT 1]\nTYPE: EFFECT_TYPE_IGNITION | CAT: NONE\n\
    CODE: NONE | PROP: NONE\nRANGE: LOCATION_HAND | LIMIT: NONE\nFLOW: PASSIVE\n--\
    \ COST:\nCost.SelfDiscard\n-- TARGET:\ns.efftg\n-- OPERATION:\ns.effop\n[EFFECT\
    \ 2]\nTYPE: EFFECT_TYPE_SINGLE, EFFECT_TYPE_TRIGGER_O | CAT: CATEGORY_TOHAND\n\
    CODE: EVENT_BE_MATERIAL | PROP: EFFECT_FLAG_DELAY\nRANGE: NONE | LIMIT: NONE\n\
    FLOW: LOCATION_GRAVE -> REASON_FUSION\n-- CONDITION:\nfunction(e,tp,eg,ep,ev,re,r,rp)\
    \ return e:GetHandler():IsLocation(LOCATION_GRAVE) and r==REASON_FUSION end\n\
    -- TARGET:\ns.exgythtg\n-- OPERATION:\ns.exgythop"
  - "[CARD] Sonic Shooter\n[STATS] Level 4 ATK 1300 DEF 600 Race 512 Attr 8\n[PSCT]\
    \ If there are no cards in your opponent's Spell & Trap Zone, this card can attack\
    \ your opponent directly. If it does, the battle damage inflicted to your opponent\
    \ is the original ATK of this card.\n[LUA]\n[EFFECT 1]\nTYPE: EFFECT_TYPE_SINGLE\
    \ | CAT: NONE\nCODE: EFFECT_DIRECT_ATTACK | PROP: NONE\nRANGE: NONE | LIMIT: NONE\n\
    FLOW: Duel.IsExistingMatchingCard -> LOCATION_SZONE\n-- CONDITION:\nfunction s.dircon(e)\n\
    \treturn not Duel.IsExistingMatchingCard(s.dfilter,e:GetHandlerPlayer(),0,LOCATION_SZONE,1,nil)\n\
    end\n-- [Filter/Helper: s.dfilter]\nfunction s.dfilter(c)\n\treturn c:GetSequence()<5\n\
    end\n[EFFECT 2]\nTYPE: EFFECT_TYPE_SINGLE | CAT: NONE\nCODE: EFFECT_CHANGE_BATTLE_DAMAGE\
    \ | PROP: NONE\nRANGE: NONE | LIMIT: NONE\nFLOW: Duel.GetAttackTarget -> Duel.GetFieldGroupCount\
    \ -> LOCATION_MZONE\n-- CONDITION:\nfunction s.rdcon(e,tp,eg,ep,ev,re,r,rp)\n\t\
    local c,tp=e:GetHandler(),e:GetHandlerPlayer()\n\treturn Duel.GetAttackTarget()==nil\
    \ and c:GetEffectCount(EFFECT_DIRECT_ATTACK)<2 and Duel.GetFieldGroupCount(tp,0,LOCATION_MZONE)>0\n\
    end"
  - "[CARD] Queen of Thorns\n[STATS] Level 6 ATK 2200 DEF 1800 Race 1024 Attr 16\n\
    [PSCT] 1 Tuner + 1 or more non-Tuner Plant-Type monsters\nEach player must pay\
    \ 1000 LP for each monster Normal or Special Summoned from their hand, except\
    \ for Plant-Type monsters.\n[LUA]\nSynchro.AddProcedure(c,nil,1,1,Synchro.NonTunerEx(Card.IsRace,RACE_PLANT),1,99)\n\
    [EFFECT 1]\nTYPE: EFFECT_TYPE_FIELD | CAT: NONE\nCODE: EFFECT_SUMMON_COST | PROP:\
    \ NONE\nRANGE: LOCATION_MZONE | LIMIT: NONE\nFLOW: Duel.CheckLPCost -> Duel.PayLPCost\n\
    -- COST:\nfunction s.ccost(e,c,tp)\n\treturn Duel.CheckLPCost(tp,1000)\nend\n\
    -- TARGET:\nfunction s.sumtg(e,c)\n\treturn c:GetRace()~=RACE_PLANT\nend\n-- OPERATION:\n\
    function s.acop(e,tp,eg,ep,ev,re,r,rp)\n\tDuel.PayLPCost(tp,1000)\nend\n[EFFECT\
    \ 2]\nTYPE: NONE | CAT: NONE\nCODE: EFFECT_SPSUMMON_COST | PROP: NONE\nRANGE:\
    \ NONE | LIMIT: NONE\nFLOW: PASSIVE"
- source_sentence: '[CARD] Al-Lumi''raj

    [STATS] Level 3 ATK 1600 DEF 1000 Race 8388608 Attr 8

    [PSCT] All monsters on the field lose ATK and DEF equal to their own Level/Rank
    x 300.

    [LUA]

    [EFFECT 1]

    TYPE: EFFECT_TYPE_FIELD | CAT: NONE

    CODE: EFFECT_UPDATE_ATTACK | PROP: NONE

    RANGE: LOCATION_MZONE | LIMIT: NONE

    FLOW: PASSIVE

    [EFFECT 2]

    TYPE: EFFECT_TYPE_FIELD | CAT: NONE

    CODE: EFFECT_UPDATE_DEFENSE | PROP: NONE

    RANGE: LOCATION_MZONE | LIMIT: NONE

    FLOW: PASSIVE'
  sentences:
  - '[CARD] Dragon''s Rage

    [STATS] Level 0 ATK 0 DEF 0 Race 0 Attr 0

    [PSCT] If your Dragon monster attacks a Defense Position monster, inflict piercing
    battle damage to your opponent.

    [LUA]

    [EFFECT 1]

    TYPE: EFFECT_TYPE_ACTIVATE | CAT: NONE

    CODE: EVENT_FREE_CHAIN | PROP: NONE

    RANGE: NONE | LIMIT: NONE

    FLOW: PASSIVE

    [EFFECT 2]

    TYPE: EFFECT_TYPE_FIELD | CAT: NONE

    CODE: EFFECT_PIERCE | PROP: NONE

    RANGE: LOCATION_SZONE | LIMIT: NONE

    FLOW: PASSIVE

    -- TARGET:

    aux.TargetBoolFunction(Card.IsRace,RACE_DRAGON)'
  - "[CARD] Des Counterblow\n[STATS] Level 0 ATK 0 DEF 0 Race 0 Attr 0\n[PSCT] Destroy\
    \ any monster that inflicts Battle Damage to a player's Life Points by attacking\
    \ directly.\n[LUA]\n[EFFECT 1]\nTYPE: EFFECT_TYPE_ACTIVATE | CAT: NONE\nCODE:\
    \ EVENT_FREE_CHAIN | PROP: NONE\nRANGE: NONE | LIMIT: NONE\nFLOW: PASSIVE\n[EFFECT\
    \ 2]\nTYPE: EFFECT_TYPE_FIELD, EFFECT_TYPE_TRIGGER_F | CAT: CATEGORY_DESTROY\n\
    CODE: EVENT_BATTLE_DAMAGE | PROP: NONE\nRANGE: LOCATION_SZONE | LIMIT: NONE\n\
    FLOW: Duel.GetAttackTarget -> Duel.SetTargetCard -> Duel.SetOperationInfo -> Duel.Destroy\
    \ -> REASON_EFFECT\n-- CONDITION:\nfunction s.condition(e,tp,eg,ep,ev,re,r,rp)\n\
    \treturn Duel.GetAttackTarget()==nil\nend\n-- TARGET:\nfunction s.target(e,tp,eg,ep,ev,re,r,rp,chk)\n\
    \tif chk==0 then return true end\n\tDuel.SetTargetCard(eg)\n\tDuel.SetOperationInfo(0,CATEGORY_DESTROY,eg,1,0,0)\n\
    end\n-- OPERATION:\nfunction s.operation(e,tp,eg,ep,ev,re,r,rp)\n\tlocal tc=eg:GetFirst()\n\
    \tif tc:IsRelateToEffect(e) then\n\t\tDuel.Destroy(tc,REASON_EFFECT)\n\tend\n\
    end"
  - "[CARD] Spell Canceller\n[STATS] Level 5 ATK 1800 DEF 1600 Race 32 Attr 8\n[PSCT]\
    \ Spell Cards, and their effects on the field, cannot be activated. Negate all\
    \ Spell effects on the field.\n[LUA]\n[EFFECT 1]\nTYPE: EFFECT_TYPE_FIELD | CAT:\
    \ NONE\nCODE: EFFECT_CANNOT_ACTIVATE | PROP: EFFECT_FLAG_PLAYER_TARGET\nRANGE:\
    \ LOCATION_MZONE | LIMIT: NONE\nFLOW: PASSIVE\n[EFFECT 2]\nTYPE: EFFECT_TYPE_FIELD\
    \ | CAT: NONE\nCODE: EFFECT_DISABLE | PROP: NONE\nRANGE: LOCATION_MZONE | LIMIT:\
    \ NONE\nFLOW: PASSIVE\n-- TARGET:\nfunction s.distg(e,c)\n\treturn c:IsSpell()\n\
    end\n[EFFECT 3]\nTYPE: EFFECT_TYPE_FIELD, EFFECT_TYPE_CONTINUOUS | CAT: NONE\n\
    CODE: EVENT_CHAIN_SOLVING | PROP: NONE\nRANGE: LOCATION_MZONE | LIMIT: NONE\n\
    FLOW: Duel.GetChainInfo -> LOCATION_SZONE -> Duel.NegateEffect\n-- OPERATION:\n\
    function s.disop(e,tp,eg,ep,ev,re,r,rp)\n\tlocal tl=Duel.GetChainInfo(ev,CHAININFO_TRIGGERING_LOCATION)\n\
    \tif (tl&LOCATION_SZONE)~=0 and re:IsSpellEffect() then\n\t\tDuel.NegateEffect(ev)\n\
    \tend\nend"
- source_sentence: '[CARD] Comrade Swordsman of Landstar

    [STATS] Level 3 ATK 500 DEF 1200 Race 1 Attr 1

    [PSCT] All Warrior-Type monsters you control gain 400 ATK.'
  sentences:
  - '[LUA]

    [EFFECT 1]

    TYPE: EFFECT_TYPE_FIELD | CAT: NONE

    CODE: EFFECT_UPDATE_ATTACK | PROP: NONE

    RANGE: LOCATION_MZONE | LIMIT: NONE

    FLOW: PASSIVE

    -- TARGET:

    aux.TargetBoolFunction(Card.IsRace,RACE_WARRIOR)'
  - '[LUA]

    [EFFECT 1]

    TYPE: EFFECT_TYPE_ACTIVATE | CAT: NONE

    CODE: EVENT_FREE_CHAIN | PROP: NONE

    RANGE: NONE | LIMIT: NONE

    FLOW: PASSIVE

    [EFFECT 2]

    TYPE: EFFECT_TYPE_FIELD | CAT: NONE

    CODE: EFFECT_TO_DECK_REDIRECT | PROP: NONE

    RANGE: LOCATION_SZONE | LIMIT: NONE

    FLOW: PASSIVE'
  - '[LUA]

    aux.AddEquipProcedure(c,nil,aux.FilterBoolFunction(Card.IsRace,RACE_INSECT))

    [EFFECT 1]

    TYPE: EFFECT_TYPE_EQUIP | CAT: NONE

    CODE: EFFECT_UPDATE_ATTACK | PROP: NONE

    RANGE: NONE | LIMIT: NONE

    FLOW: PASSIVE

    [EFFECT 2]

    TYPE: NONE | CAT: NONE

    CODE: EFFECT_UPDATE_DEFENSE | PROP: NONE

    RANGE: NONE | LIMIT: NONE

    FLOW: PASSIVE'
- source_sentence: '[CARD] Ally of Justice Quarantine

    [STATS] Level 4 ATK 1700 DEF 1200 Race 32 Attr 32

    [PSCT] Neither player can Special Summon LIGHT monsters.'
  sentences:
  - '[LUA]

    aux.AddEquipProcedure(c,nil,aux.FilterBoolFunction(Card.IsRace,RACE_PLANT))

    [EFFECT 1]

    TYPE: EFFECT_TYPE_EQUIP | CAT: NONE

    CODE: EFFECT_UPDATE_ATTACK | PROP: NONE

    RANGE: NONE | LIMIT: NONE

    FLOW: PASSIVE

    [EFFECT 2]

    TYPE: EFFECT_TYPE_EQUIP | CAT: NONE

    CODE: EFFECT_UPDATE_DEFENSE | PROP: NONE

    RANGE: NONE | LIMIT: NONE

    FLOW: PASSIVE'
  - '[LUA]

    aux.AddEquipProcedure(c,nil,aux.FilterBoolFunction(Card.IsRace,RACE_FIEND))

    [EFFECT 1]

    TYPE: EFFECT_TYPE_EQUIP | CAT: NONE

    CODE: EFFECT_UPDATE_ATTACK | PROP: NONE

    RANGE: NONE | LIMIT: NONE

    FLOW: PASSIVE

    [EFFECT 2]

    TYPE: EFFECT_TYPE_EQUIP | CAT: NONE

    CODE: EFFECT_UPDATE_DEFENSE | PROP: NONE

    RANGE: NONE | LIMIT: NONE

    FLOW: PASSIVE'
  - '[LUA]

    [EFFECT 1]

    TYPE: EFFECT_TYPE_FIELD | CAT: NONE

    CODE: EFFECT_CANNOT_SPECIAL_SUMMON | PROP: EFFECT_FLAG_PLAYER_TARGET

    RANGE: LOCATION_MZONE | LIMIT: NONE

    FLOW: PASSIVE

    -- TARGET:

    aux.TargetBoolFunction(Card.IsAttribute,ATTRIBUTE_LIGHT)'
- source_sentence: '[CARD] Enraged Battle Ox

    [STATS] Level 4 ATK 1700 DEF 1000 Race 32768 Attr 1

    [PSCT] If your Beast, Beast-Warrior, or Winged Beast monster attacks a Defense
    Position monster, inflict piercing battle damage.'
  sentences:
  - '[LUA]

    [EFFECT 1]

    TYPE: EFFECT_TYPE_IGNITION | CAT: CATEGORY_DESTROY

    CODE: NONE | PROP: EFFECT_FLAG_CARD_TARGET

    RANGE: LOCATION_MZONE | LIMIT: NONE

    FLOW: PASSIVE

    -- TARGET:

    s.target

    -- OPERATION:

    s.operation'
  - "[LUA]\n[EFFECT 1]\nTYPE: EFFECT_TYPE_FIELD | CAT: NONE\nCODE: EFFECT_PIERCE |\
    \ PROP: NONE\nRANGE: LOCATION_MZONE | LIMIT: NONE\nFLOW: PASSIVE\n-- TARGET:\n\
    function s.target(e,c)\n\treturn c:IsRace(RACES_BEAST_BWARRIOR_WINGB)\nend"
  - '[LUA]

    [EFFECT 1]

    TYPE: EFFECT_TYPE_SINGLE | CAT: NONE

    CODE: EFFECT_UPDATE_ATTACK | PROP: EFFECT_FLAG_SINGLE_RANGE

    RANGE: LOCATION_MZONE | LIMIT: NONE

    FLOW: PASSIVE'
pipeline_tag: sentence-similarity
library_name: sentence-transformers
---

# SentenceTransformer based on microsoft/unixcoder-base

This is a [sentence-transformers](https://www.SBERT.net) model finetuned from [microsoft/unixcoder-base](https://huggingface.co/microsoft/unixcoder-base). It maps inputs to a 768-dimensional dense vector space and can be used for semantic textual similarity, semantic search, paraphrase mining, classification, clustering, and more.

## Model Details

### Model Description
- **Model Type:** Sentence Transformer
- **Base model:** [microsoft/unixcoder-base](https://huggingface.co/microsoft/unixcoder-base) <!-- at revision 5604afdc964f6c53782a6813140ade5216b99006 -->
- **Maximum Sequence Length:** 512 tokens
- **Output Dimensionality:** 768 dimensions
- **Similarity Function:** Cosine Similarity
- **Supported Modality:** Text
<!-- - **Training Dataset:** Unknown -->
<!-- - **Language:** Unknown -->
<!-- - **License:** Unknown -->

### Model Sources

- **Documentation:** [Sentence Transformers Documentation](https://sbert.net)
- **Repository:** [Sentence Transformers on GitHub](https://github.com/huggingface/sentence-transformers)
- **Hugging Face:** [Sentence Transformers on Hugging Face](https://huggingface.co/models?library=sentence-transformers)

### Full Model Architecture

```
SentenceTransformer(
  (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'RobertaModel'})
  (1): Pooling({'embedding_dimension': 768, 'pooling_mode': 'mean', 'include_prompt': True})
)
```

## Usage

### Direct Usage (Sentence Transformers)

First install the Sentence Transformers library:

```bash
pip install -U sentence-transformers
```
Then you can load this model and run inference.
```python
from sentence_transformers import SentenceTransformer

# Download from the 🤗 Hub
model = SentenceTransformer("sentence_transformers_model_id")
# Run inference
sentences = [
    '[CARD] Enraged Battle Ox\n[STATS] Level 4 ATK 1700 DEF 1000 Race 32768 Attr 1\n[PSCT] If your Beast, Beast-Warrior, or Winged Beast monster attacks a Defense Position monster, inflict piercing battle damage.',
    '[LUA]\n[EFFECT 1]\nTYPE: EFFECT_TYPE_FIELD | CAT: NONE\nCODE: EFFECT_PIERCE | PROP: NONE\nRANGE: LOCATION_MZONE | LIMIT: NONE\nFLOW: PASSIVE\n-- TARGET:\nfunction s.target(e,c)\n\treturn c:IsRace(RACES_BEAST_BWARRIOR_WINGB)\nend',
    '[LUA]\n[EFFECT 1]\nTYPE: EFFECT_TYPE_IGNITION | CAT: CATEGORY_DESTROY\nCODE: NONE | PROP: EFFECT_FLAG_CARD_TARGET\nRANGE: LOCATION_MZONE | LIMIT: NONE\nFLOW: PASSIVE\n-- TARGET:\ns.target\n-- OPERATION:\ns.operation',
]
embeddings = model.encode(sentences)
print(embeddings.shape)
# [3, 768]

# Get the similarity scores for the embeddings
similarities = model.similarity(embeddings, embeddings)
print(similarities)
# tensor([[1.0000, 0.7426, 0.0114],
#         [0.7426, 1.0000, 0.2058],
#         [0.0114, 0.2058, 1.0000]])
```
<!--
### Direct Usage (Transformers)

<details><summary>Click to see the direct usage in Transformers</summary>

</details>
-->

<!--
### Downstream Usage (Sentence Transformers)

You can finetune this model on your own dataset.

<details><summary>Click to expand</summary>

</details>
-->

<!--
### Out-of-Scope Use

*List how the model may foreseeably be misused and address what users ought not to do with the model.*
-->

<!--
## Bias, Risks and Limitations

*What are the known or foreseeable issues stemming from this model? You could also flag here known failure cases or weaknesses of the model.*
-->

<!--
### Recommendations

*What are recommendations with respect to the foreseeable issues? For example, filtering explicit content.*
-->

## Training Details

### Training Datasets

#### Unnamed Dataset

* Size: 26,490 training samples
* Columns: <code>sentence_0</code> and <code>sentence_1</code>
* Approximate statistics based on the first 100 samples:
  |          | sentence_0                                                                           | sentence_1                                                                           |
  |:---------|:-------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------|
  | type     | string                                                                               | string                                                                               |
  | modality | text                                                                                 | text                                                                                 |
  | details  | <ul><li>min: 38 tokens</li><li>mean: 290.83 tokens</li><li>max: 512 tokens</li></ul> | <ul><li>min: 97 tokens</li><li>mean: 462.33 tokens</li><li>max: 512 tokens</li></ul> |
* Samples:
  | sentence_0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | sentence_1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
  |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | <code>[CARD] The Phantom Knights of Malevolent Scythe<br>[STATS] Level 3 ATK 1900 DEF 0 Race 1 Attr 32<br>[PSCT] 2 Level 3 DARK monsters  <br>You can detach 1 material from this card; Special Summon 1 "The Phantom Knights" monster from your Deck. If you Xyz Summon an "Xyz Dragon" monster, while this card is in your Monster Zone (except during the Damage Step): You can add 1 "Rank-Up-Magic" Spell from your Deck to your hand. If this card is destroyed: You can add 1 of your banished "The Phantom Knights" cards to your hand, except Xyz Monsters. You can only use each effect of "The Phantom Knights of Malevolent Scythe" once per turn.</code> | <code>[LUA]<br>Xyz.AddProcedure(c,aux.FilterBoolFunctionEx(Card.IsAttribute,ATTRIBUTE_DARK),3,2)<br>[EFFECT 1]<br>TYPE: EFFECT_TYPE_IGNITION \| CAT: CATEGORY_SPECIAL_SUMMON<br>CODE: NONE \| PROP: NONE<br>RANGE: LOCATION_MZONE \| LIMIT: 1,{id,0}<br>FLOW: Duel.GetLocationCount -> LOCATION_MZONE -> Duel.IsExistingMatchingCard -> LOCATION_DECK -> Duel.SetOperationInfo -> Duel.Hint -> Duel.SelectMatchingCard -> Duel.SpecialSummon -> POS_FACEUP<br>-- COST:<br>Cost.DetachFromSelf(1)<br>-- TARGET:<br>function s.sptg(e,tp,eg,ep,ev,re,r,rp,chk)<br>	if chk==0 then return Duel.GetLocationCount(tp,LOCATION_MZONE)>0<br>		and Duel.IsExistingMatchingCard(s.spfilter,tp,LOCATION_DECK,0,1,nil,e,tp) end<br>	Duel.SetOperationInfo(0,CATEGORY_SPECIAL_SUMMON,nil,1,tp,LOCATION_DECK)<br>end<br>-- [Filter/Helper: s.spfilter]<br>function s.spfilter(c,e,tp)<br>	return c:IsSetCard(SET_THE_PHANTOM_KNIGHTS) and c:IsCanBeSpecialSummoned(e,0,tp,false,false)<br>end<br>-- OPERATION:<br>function s.spop(e,tp,eg,ep,ev,re,r,rp)<br>	if Duel.GetLocationCount(tp,LOCATION_MZONE)<=0 then return end<br>	...</code> |
  | <code>[CARD] Gemini Spark<br>[STATS] Level 0 ATK 0 DEF 0 Race 0 Attr 0<br>[PSCT] Tribute 1 face-up Level 4 Gemini monster, then target 1 card on the field; destroy it, and if you do, draw 1 card.</code>                                                                                                                                                                                                                                                                                                                                                                                                                                                           | <code>[LUA]<br>[EFFECT 1]<br>TYPE: EFFECT_TYPE_ACTIVATE \| CAT: CATEGORY_DESTROY<br>CODE: EVENT_FREE_CHAIN \| PROP: EFFECT_FLAG_CARD_TARGET<br>RANGE: NONE \| LIMIT: NONE<br>FLOW: Duel.GetMatchingGroup -> LOCATION_ONFIELD -> Duel.GetFieldGroupCount -> LOCATION_DECK -> Duel.CheckReleaseGroupCost -> Duel.IsExistingTarget -> Duel.SelectReleaseGroupCost -> Duel.Release -> REASON_COST -> Duel.Hint -> Duel.SelectTarget -> Duel.SetOperationInfo -> Duel.GetFirstTarget -> Duel.Destroy -> REASON_EFFECT -> Duel.Draw<br>-- COST:<br>function s.cost(e,tp,eg,ep,ev,re,r,rp,chk)<br>	e:SetLabel(1)<br>	return true<br>end<br>-- TARGET:<br>function s.target(e,tp,eg,ep,ev,re,r,rp,chk,chkc)<br>	if chkc then return chkc:IsOnField() and chkc~=e:GetHandler() end<br>	local dg=Duel.GetMatchingGroup(Card.IsCanBeEffectTarget,tp,LOCATION_ONFIELD,LOCATION_ONFIELD,e:GetHandler(),e)<br>	if chk==0 then<br>		if Duel.GetFieldGroupCount(tp,LOCATION_DECK,0)==0 then return false end<br>		if e:GetLabel()==1 then<br>			e:SetLabel(0)<br>			return Duel.CheckReleaseGroupCost(tp,s.cfilter,1,false...</code>          |
  | <code>[CARD] Battlin' Boxer Sparrer<br>[STATS] Level 4 ATK 1200 DEF 1400 Race 1 Attr 4<br>[PSCT] If you control a "Battlin' Boxer" monster, you can Special Summon this card (from your hand). If you do, you cannot conduct your Battle Phase for the rest of this turn.</code>                                                                                                                                                                                                                                                                                                                                                                                     | <code>[LUA]<br>[EFFECT 1]<br>TYPE: EFFECT_TYPE_FIELD \| CAT: NONE<br>CODE: EFFECT_SPSUMMON_PROC \| PROP: EFFECT_FLAG_UNCOPYABLE<br>RANGE: LOCATION_HAND \| LIMIT: NONE<br>FLOW: Duel.GetLocationCount -> LOCATION_MZONE -> Duel.IsExistingMatchingCard -> Duel.RegisterEffect<br>-- CONDITION:<br>function s.spcon(e,c)<br>	if c==nil then return true end<br>	local tp=c:GetControler()<br>	return Duel.GetLocationCount(tp,LOCATION_MZONE)>0 and<br>		Duel.IsExistingMatchingCard(aux.FaceupFilter(Card.IsSetCard,SET_BATTLIN_BOXER),tp,LOCATION_MZONE,0,1,nil)<br>end<br>-- OPERATION:<br>function s.spop(e,tp,eg,ep,ev,re,r,rp,c)<br>	local e1=Effect.CreateEffect(e:GetHandler())<br>	e1:SetType(EFFECT_TYPE_FIELD)<br>	e1:SetCode(EFFECT_CANNOT_BP)<br>	e1:SetProperty(EFFECT_FLAG_PLAYER_TARGET+EFFECT_FLAG_OATH)<br>	e1:SetTargetRange(1,0)<br>	e1:SetReset(RESET_PHASE\|PHASE_END)<br>	Duel.RegisterEffect(e1,tp)<br>	aux.RegisterClientHint(e:GetHandler(),nil,tp,1,0,aux.Stringid(id,0),nil)<br>end</code>                                                                                                         |
* Loss: [<code>MultipleNegativesRankingLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#multiplenegativesrankingloss) with these parameters:
  ```json
  {
      "scale": 20.0,
      "similarity_fct": "cos_sim",
      "gather_across_devices": false,
      "directions": [
          "query_to_doc"
      ],
      "partition_mode": "joint",
      "hardness_mode": null,
      "hardness_strength": 0.0
  }
  ```

#### Unnamed Dataset

* Size: 39,730 training samples
* Columns: <code>sentence_0</code>, <code>sentence_1</code>, and <code>label</code>
* Approximate statistics based on the first 100 samples:
  |          | sentence_0                                                                            | sentence_1                                                                            | label                                                           |
  |:---------|:--------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------|:----------------------------------------------------------------|
  | type     | string                                                                                | string                                                                                | float                                                           |
  | modality | text                                                                                  | text                                                                                  |                                                                 |
  | details  | <ul><li>min: 104 tokens</li><li>mean: 491.51 tokens</li><li>max: 512 tokens</li></ul> | <ul><li>min: 120 tokens</li><li>mean: 490.35 tokens</li><li>max: 512 tokens</li></ul> | <ul><li>min: 0.0</li><li>mean: 0.16</li><li>max: 0.45</li></ul> |
* Samples:
  | sentence_0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | sentence_1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | label                             |
  |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:----------------------------------|
  | <code>[CARD] Springans Branga<br>[STATS] Level 8 ATK 500 DEF 2500 Race 32 Attr 4<br>[PSCT] If this card is in your hand, field, or GY: You can target 1 "Springans" Xyz Monster you control; attach this card to it as material. You can banish this card and 1 "Springans" monster with a different name from your GY; add 1 "Springans" card from your Deck to your hand. You can only use each effect of "Springans Branga" once per turn.<br>[LUA]<br>[EFFECT 1]<br>TYPE: EFFECT_TYPE_IGNITION \| CAT: NONE<br>CODE: NONE \| PROP: EFFECT_FLAG_CARD_TARGET<br>RANGE: LOCATION_GRAVE\|LOCATION_HAND\|LOCATION_MZONE \| LIMIT: 1,id<br>FLOW: LOCATION_MZONE -> Duel.IsExistingTarget -> Duel.Hint -> Duel.SelectTarget -> LOCATION_GRAVE -> Duel.SetOperationInfo -> Duel.GetFirstTarget -> Duel.Overlay<br>-- TARGET:<br>function s.mattg(e,tp,eg,ep,ev,re,r,rp,chk,chkc)<br>	if chkc then return chkc:IsLocation(LOCATION_MZONE) and chkc:IsControler(tp) and s.matfilter(chkc) end<br>	if chk==0 then return Duel.IsExistingTarget(s.matfilter,tp,LOCATION_MZONE,0,1,nil) end<br>	Due...</code>           | <code>[CARD] The Tripper Mercury<br>[STATS] Level 8 ATK 2000 DEF 2000 Race 64 Attr 2<br>[PSCT] When this card is Tribute Summoned: You can change all monsters on the field to face-up Attack Position. You can Tribute 3 monsters to Tribute Summon (but not Set) this card. If Summoned this way, while this card is on the field all monsters your opponent controls lose ATK equal to their original ATK. This card can make a second attack during each Battle Phase.<br>[LUA]<br>[EFFECT 1]<br>TYPE: EFFECT_TYPE_SINGLE, EFFECT_TYPE_TRIGGER_O \| CAT: CATEGORY_POSITION<br>CODE: EVENT_SUMMON_SUCCESS \| PROP: NONE<br>RANGE: NONE \| LIMIT: NONE<br>FLOW: Duel.IsExistingMatchingCard -> LOCATION_MZONE -> Duel.GetMatchingGroup -> Duel.ChangePosition -> POS_FACEUP_ATTACK<br>-- CONDITION:<br>function s.poscon(e,tp,eg,ep,ev,re,r,rp)<br>	return e:GetHandler():IsTributeSummoned()<br>end<br>-- TARGET:<br>function s.postg(e,tp,eg,ep,ev,re,r,rp,chk)<br>	if chk==0 then return Duel.IsExistingMatchingCard(s.posfilter,tp,LOCATION_MZONE,LOCATION_MZONE,1,nil) end<br>end<br>-- [Filt...</code>          | <code>0.058823529411764705</code> |
  | <code>[CARD] Shinobird Crane<br>[STATS] Level 4 ATK 1500 DEF 1500 Race 512 Attr 8<br>[PSCT] Cannot be Special Summoned. Once per turn, if another Spirit monster is Normal or Special Summoned while this monster is on the field: You can draw 1 card. Once per turn, during the End Phase, if this card was Normal Summoned or flipped face-up this turn: Return it to the hand.<br>[LUA]<br>[EFFECT 1]<br>TYPE: EFFECT_TYPE_SINGLE \| CAT: NONE<br>CODE: EFFECT_SPSUMMON_CONDITION \| PROP: EFFECT_FLAG_CANNOT_DISABLE, EFFECT_FLAG_UNCOPYABLE<br>RANGE: NONE \| LIMIT: NONE<br>FLOW: PASSIVE<br>[EFFECT 2]<br>TYPE: EFFECT_TYPE_FIELD, EFFECT_TYPE_TRIGGER_O \| CAT: CATEGORY_DRAW<br>CODE: EVENT_SPSUMMON_SUCCESS \| PROP: EFFECT_FLAG_PLAYER_TARGET, EFFECT_FLAG_DELAY<br>RANGE: LOCATION_MZONE \| LIMIT: 1,0,EFFECT_COUNT_CODE_SINGLE<br>FLOW: Duel.IsPlayerCanDraw -> Duel.SetTargetPlayer -> Duel.SetTargetParam -> Duel.SetOperationInfo -> Duel.GetChainInfo -> Duel.Draw -> REASON_EFFECT<br>-- CONDITION:<br>function s.condition(e,tp,eg,ep,ev,re,r,rp)<br>	return not eg:IsContains(e...</code> | <code>[CARD] Vylon Prism<br>[STATS] Level 4 ATK 1500 DEF 1500 Race 4096 Attr 16<br>[PSCT] If this card is sent from the Monster Zone to the GY: You can pay 500 Life Points, then target 1 face-up monster you control; equip this card to that target. If the equipped monster battles, it gains 1000 ATK during the Damage Step only.  <br>  <br>* The above text is unofficial and describes the card's functionality in the OCG.<br>[LUA]<br>[EFFECT 1]<br>TYPE: EFFECT_TYPE_SINGLE, EFFECT_TYPE_TRIGGER_O \| CAT: CATEGORY_EQUIP<br>CODE: EVENT_TO_GRAVE \| PROP: EFFECT_FLAG_CARD_TARGET, EFFECT_FLAG_DELAY<br>RANGE: NONE \| LIMIT: NONE<br>FLOW: LOCATION_MZONE -> Duel.GetLocationCount -> LOCATION_SZONE -> Duel.IsExistingTarget -> Duel.Hint -> Duel.SelectTarget -> Duel.SetOperationInfo -> Duel.GetFirstTarget -> Duel.Equip<br>-- CONDITION:<br>function s.eqcon(e,tp,eg,ep,ev,re,r,rp)<br>	local c=e:GetHandler()<br>	return c:GetPreviousLocation()==LOCATION_MZONE<br>end<br>-- COST:<br>Cost.PayLP(500)<br>-- TARGET:<br>function s.eqtg(e,tp,eg,ep,ev,re,r,rp,chk,chkc)<br>	if chkc then r...</code> | <code>0.12121212121212122</code>  |
  | <code>[CARD] Synchro Fusionist<br>[STATS] Level 2 ATK 800 DEF 600 Race 2 Attr 32<br>[PSCT] If this card is sent to the Graveyard as a Synchro Material Monster, you can add 1 Spell Card from your Deck to your hand with "Polymerization" or "Fusion" in the card name, except "Diffusion Wave-Motion".<br>[LUA]<br>[EFFECT 1]<br>TYPE: EFFECT_TYPE_SINGLE, EFFECT_TYPE_TRIGGER_O \| CAT: CATEGORY_TOHAND, CATEGORY_SEARCH<br>CODE: EVENT_BE_MATERIAL \| PROP: EFFECT_FLAG_DELAY<br>RANGE: NONE \| LIMIT: NONE<br>FLOW: LOCATION_GRAVE -> REASON_SYNCHRO -> Duel.IsExistingMatchingCard -> LOCATION_DECK -> Duel.SetOperationInfo -> Duel.Hint -> Duel.SelectMatchingCard -> Duel.SendtoHand -> REASON_EFFECT -> Duel.ConfirmCards<br>-- CONDITION:<br>function s.condition(e,tp,eg,ep,ev,re,r,rp)<br>	return e:GetHandler():IsLocation(LOCATION_GRAVE) and r==REASON_SYNCHRO<br>end<br>-- TARGET:<br>function s.target(e,tp,eg,ep,ev,re,r,rp,chk)<br>	if chk==0 then return Duel.IsExistingMatchingCard(s.filter,tp,LOCATION_DECK,0,1,nil) end<br>	Duel.SetOperationInfo(0,CATEGORY_TOHAND,nil,...</code>    | <code>[CARD] Gigantes<br>[STATS] Level 4 ATK 1900 DEF 1300 Race 256 Attr 1<br>[PSCT] Cannot be Normal Summoned/Set. Must first be Special Summoned (from your hand) by banishing 1 EARTH monster from your GY. If this card is destroyed by battle and sent to the GY: Destroy all Spells and Traps on the field.<br>[LUA]<br>[EFFECT 1]<br>TYPE: EFFECT_TYPE_FIELD \| CAT: NONE<br>CODE: EFFECT_SPSUMMON_PROC \| PROP: EFFECT_FLAG_UNCOPYABLE<br>RANGE: LOCATION_HAND \| LIMIT: NONE<br>FLOW: Duel.GetMatchingGroup -> LOCATION_MZONE -> LOCATION_GRAVE -> Duel.GetLocationCount -> Duel.Remove -> POS_FACEUP -> REASON_COST<br>-- CONDITION:<br>function s.spcon(e,c)<br>	if c==nil then return true end<br>	local tp=e:GetHandlerPlayer()<br>	local rg=Duel.GetMatchingGroup(s.spfilter,tp,LOCATION_MZONE\|LOCATION_GRAVE,0,nil,tp)<br>	local ft=Duel.GetLocationCount(tp,LOCATION_MZONE)<br>	return ft>-1 and #rg>0 and aux.SelectUnselectGroup(rg,e,tp,1,1,nil,0)<br>end<br>-- [Filter/Helper: s.spfilter]<br>function s.spfilter(c,tp)<br>	return c:IsAttribute(ATTRIBUTE_EARTH) and c:IsAbleToRemove...</code>   | <code>0.125</code>                |
* Loss: [<code>CoSENTLoss</code>](https://sbert.net/docs/package_reference/sentence_transformer/losses.html#cosentloss) with these parameters:
  ```json
  {
      "scale": 20.0,
      "similarity_fct": "pairwise_cos_sim"
  }
  ```

### Training Hyperparameters
#### Non-Default Hyperparameters

- `per_device_train_batch_size`: 16
- `fp16`: True
- `per_device_eval_batch_size`: 16
- `multi_dataset_batch_sampler`: round_robin

#### All Hyperparameters
<details><summary>Click to expand</summary>

- `per_device_train_batch_size`: 16
- `num_train_epochs`: 3
- `max_steps`: -1
- `learning_rate`: 5e-05
- `lr_scheduler_type`: linear
- `lr_scheduler_kwargs`: None
- `warmup_steps`: 0
- `optim`: adamw_torch_fused
- `optim_args`: None
- `weight_decay`: 0.0
- `adam_beta1`: 0.9
- `adam_beta2`: 0.999
- `adam_epsilon`: 1e-08
- `optim_target_modules`: None
- `gradient_accumulation_steps`: 1
- `average_tokens_across_devices`: True
- `max_grad_norm`: 1
- `label_smoothing_factor`: 0.0
- `bf16`: False
- `fp16`: True
- `bf16_full_eval`: False
- `fp16_full_eval`: False
- `tf32`: None
- `gradient_checkpointing`: False
- `gradient_checkpointing_kwargs`: None
- `torch_compile`: False
- `torch_compile_backend`: None
- `torch_compile_mode`: None
- `use_liger_kernel`: False
- `liger_kernel_config`: None
- `use_cache`: False
- `neftune_noise_alpha`: None
- `torch_empty_cache_steps`: None
- `auto_find_batch_size`: False
- `log_on_each_node`: True
- `logging_nan_inf_filter`: True
- `include_num_input_tokens_seen`: no
- `log_level`: passive
- `log_level_replica`: warning
- `disable_tqdm`: False
- `project`: huggingface
- `trackio_space_id`: None
- `trackio_bucket_id`: None
- `trackio_static_space_id`: None
- `per_device_eval_batch_size`: 16
- `prediction_loss_only`: True
- `eval_on_start`: False
- `eval_do_concat_batches`: True
- `eval_use_gather_object`: False
- `eval_accumulation_steps`: None
- `include_for_metrics`: []
- `batch_eval_metrics`: False
- `save_only_model`: False
- `save_on_each_node`: False
- `enable_jit_checkpoint`: False
- `push_to_hub`: False
- `hub_private_repo`: None
- `hub_model_id`: None
- `hub_strategy`: every_save
- `hub_always_push`: False
- `hub_revision`: None
- `load_best_model_at_end`: False
- `ignore_data_skip`: False
- `restore_callback_states_from_checkpoint`: False
- `full_determinism`: False
- `seed`: 42
- `data_seed`: None
- `use_cpu`: False
- `accelerator_config`: {'split_batches': False, 'dispatch_batches': None, 'even_batches': True, 'use_seedable_sampler': True, 'non_blocking': False, 'gradient_accumulation_kwargs': None}
- `parallelism_config`: None
- `dataloader_drop_last`: False
- `dataloader_num_workers`: 0
- `dataloader_pin_memory`: True
- `dataloader_persistent_workers`: False
- `dataloader_prefetch_factor`: None
- `dataloader_multiprocessing_context`: None
- `dataloader_in_order`: True
- `remove_unused_columns`: True
- `label_names`: None
- `train_sampling_strategy`: random
- `length_column_name`: length
- `ddp_find_unused_parameters`: None
- `ddp_bucket_cap_mb`: None
- `ddp_broadcast_buffers`: False
- `ddp_static_graph`: None
- `ddp_backend`: None
- `ddp_timeout`: 1800
- `fsdp`: None
- `fsdp_config`: None
- `deepspeed`: None
- `debug`: []
- `skip_memory_metrics`: True
- `do_predict`: False
- `resume_from_checkpoint`: None
- `local_rank`: -1
- `prompts`: None
- `batch_sampler`: batch_sampler
- `multi_dataset_batch_sampler`: round_robin
- `router_mapping`: {}
- `learning_rate_mapping`: {}
- `warmup_ratio`: None

</details>

### Training Logs
| Epoch  | Step | Training Loss |
|:------:|:----:|:-------------:|
| 0.1510 | 500  | 2.8477        |
| 0.3019 | 1000 | 2.4222        |
| 0.4529 | 1500 | 2.3009        |
| 0.6039 | 2000 | 2.2333        |
| 0.7548 | 2500 | 2.2247        |
| 0.9058 | 3000 | 2.2018        |
| 1.0568 | 3500 | 2.1608        |
| 1.2077 | 4000 | 2.1127        |
| 1.3587 | 4500 | 2.1274        |
| 1.5097 | 5000 | 2.0824        |
| 1.6606 | 5500 | 2.0878        |
| 1.8116 | 6000 | 2.0569        |
| 1.9626 | 6500 | 2.0629        |
| 2.1135 | 7000 | 2.0037        |
| 2.2645 | 7500 | 1.9941        |
| 2.4155 | 8000 | 2.0010        |
| 2.5664 | 8500 | 1.9566        |
| 2.7174 | 9000 | 1.9697        |
| 2.8684 | 9500 | 1.9666        |


### Training Time
- **Training**: 45.1 minutes

### Framework Versions
- Python: 3.14.8
- Sentence Transformers: 6.2.0
- Transformers: 5.22.1
- PyTorch: 2.15.0+rocm10.0
- Accelerate: 1.15.0
- Datasets: 5.1.0
- Tokenizers: 0.23.3

## Additional Resources

- [Training and Finetuning Embedding Models with Sentence Transformers](https://huggingface.co/blog/train-sentence-transformers): the end-to-end guide for training or finetuning Sentence Transformer models.
- [Introduction to Matryoshka Embedding Models](https://huggingface.co/blog/matryoshka): variable-size embeddings that can be truncated with minimal quality loss.
- [Binary and Scalar Embedding Quantization for Significantly Faster & Cheaper Retrieval](https://huggingface.co/blog/embedding-quantization): post-training compression of embedding vectors.
- [Multimodal Embedding & Reranker Models with Sentence Transformers](https://huggingface.co/blog/multimodal-sentence-transformers): use text, image, audio, and video models through the same API.
- [Training and Finetuning Multimodal Embedding & Reranker Models with Sentence Transformers](https://huggingface.co/blog/train-multimodal-sentence-transformers): train multimodal embedding models, with a Visual Document Retrieval walkthrough.

## Citation

### BibTeX

#### Sentence Transformers
```bibtex
@inproceedings{reimers-2019-sentence-bert,
    title = "Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks",
    author = "Reimers, Nils and Gurevych, Iryna",
    booktitle = "Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing",
    month = "11",
    year = "2019",
    publisher = "Association for Computational Linguistics",
    url = "https://arxiv.org/abs/1908.10084",
}
```

#### MultipleNegativesRankingLoss
```bibtex
@misc{oord2019representationlearningcontrastivepredictive,
      title={Representation Learning with Contrastive Predictive Coding},
      author={Aaron van den Oord and Yazhe Li and Oriol Vinyals},
      year={2019},
      eprint={1807.03748},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/1807.03748},
}
```

#### CoSENTLoss
```bibtex
@article{10531646,
    author={Huang, Xiang and Peng, Hao and Zou, Dongcheng and Liu, Zhiwei and Li, Jianxin and Liu, Kay and Wu, Jia and Su, Jianlin and Yu, Philip S.},
    journal={IEEE/ACM Transactions on Audio, Speech, and Language Processing},
    title={CoSENT: Consistent Sentence Embedding via Similarity Ranking},
    year={2024},
    doi={10.1109/TASLP.2024.3402087}
}
```

<!--
## Glossary

*Clearly define terms in order to be accessible across audiences.*
-->

<!--
## Model Card Authors

*Lists the people who create the model card, providing recognition and accountability for the detailed work that goes into its construction.*
-->

<!--
## Model Card Contact

*Provides a way for people who have updates to the Model Card, suggestions, or questions, to contact the Model Card authors.*
-->