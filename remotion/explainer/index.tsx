// 🎬 Entry for the explainer video. scripts/make_explainer.py stages this folder inside OpenMontage's
// remotion-composer and renders it. 90 seconds, 1920x1080, 30 fps.
import React from "react";
import { Composition, registerRoot } from "remotion";
import { Explainer, type ExplainerProps } from "./Explainer";

const defaultProps: ExplainerProps = {
  durationSeconds: 90,
  audioSrc: null,
  shots: [{ id: "title", label: "01 · Title", start: 0, end: 90 }],
  captions: [],
};

const Root: React.FC = () => (
  <Composition
    id="Explainer"
    component={Explainer}
    fps={30}
    width={1920}
    height={1080}
    durationInFrames={90 * 30}
    defaultProps={defaultProps}
    calculateMetadata={({ props }) => ({ durationInFrames: Math.round((props.durationSeconds ?? 90) * 30) })}
  />
);

registerRoot(Root);
