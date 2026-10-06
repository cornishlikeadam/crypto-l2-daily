// 🎞️ Entry for the daily card deck. Staged by scripts/render.py into
// OpenMontage/projects/crypto-l2-YYYY-MM-DD/composition/ and rendered through
// OpenMontage's video_compose atelier path. Original code; depends only on
// the remotion packages installed in OpenMontage/remotion-composer.
import React from "react";
import { Composition, registerRoot } from "remotion";
import { CardDeck, type DeckProps } from "./CardDeck";

const FPS = 30;

const defaultProps: DeckProps = {
  durationSeconds: 70,
  audioSrc: null,
  cards: [
    { id: "title", kind: "title", title: "Crypto L2 Daily", sentence: "Preview", corner: "X search",
      corner_sub: "last 24 hours", coin: null, start: 0, end: 70 },
  ],
};

const Root: React.FC = () => (
  <Composition
    id="CryptoCards"
    component={CardDeck}
    fps={FPS}
    width={1920}
    height={1080}
    durationInFrames={70 * FPS}
    defaultProps={defaultProps}
    calculateMetadata={({ props }) => ({
      durationInFrames: Math.round((props.durationSeconds ?? 70) * FPS),
    })}
  />
);

registerRoot(Root);
