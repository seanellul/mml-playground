/* eslint-disable @typescript-eslint/no-unused-vars */
import {
  IMMLScene,
  Interaction,
  InteractionListener,
  InteractionManager,
  MMLClickTrigger,
  PromptManager,
  PromptProps,
  registerCustomElementsToWindow,
  setGlobalMScene,
  PositionAndRotation,
} from "mml-web";
import { AudioListener, Group, PerspectiveCamera, Scene, WebGLRenderer } from "three";

export class CoreMMLScene {
  private scene: THREE.Scene;
  private camera: THREE.Camera;
  private mmlScene: Partial<IMMLScene>;
  private getUserPositionAndRotation: () => PositionAndRotation;
  private promptManager: PromptManager;
  private interactionListener: InteractionListener;
  private elementsHolder: HTMLElement;

  private audioListener: AudioListener;
  private clickTrigger: MMLClickTrigger;

  constructor(
    group: Group,
    elementsHolder: HTMLElement,
    renderer: WebGLRenderer,
    scene: Scene,
    camera: PerspectiveCamera,
    getUserPositionAndRotation: () => PositionAndRotation,
  ) {
    this.scene = scene;
    this.camera = camera;
    this.elementsHolder = elementsHolder;
    this.getUserPositionAndRotation = getUserPositionAndRotation;

    this.audioListener = new AudioListener();

    document.addEventListener("mousedown", this.onMouseDown.bind(this));

    this.mmlScene = {
      getAudioListener: () => this.audioListener,
      getRenderer: () => renderer,
      getThreeScene: () => scene,
      getRootContainer: () => group,
      getCamera: () => camera,
      getUserPositionAndRotation: this.getUserPositionAndRotation,
      addCollider: () => {},
      updateCollider: () => {},
      removeCollider: () => {},
      addInteraction: (interaction: Interaction) => {
        this.interactionListener.addInteraction(interaction);
      },
      updateInteraction: (interaction: Interaction) => {
        this.interactionListener.updateInteraction(interaction);
      },
      removeInteraction: (interaction: Interaction) => {
        this.interactionListener.removeInteraction(interaction);
      },
      prompt: (promptProps: PromptProps, callback: (message: string | null) => void) => {
        this.promptManager.prompt(promptProps, callback);
      },
    };
  }

  onMouseDown() {
    if (this.audioListener.context.state === "suspended") {
      this.audioListener.context.resume();
    }
  }

  traverseDOM(node: Node | null, callback: (node: Node) => void): void {
    if (node === null) return;
    const notGarbage = node.nodeType !== 3 && node.nodeType !== 8;
    const isMML = node.nodeName.toLowerCase().includes("m-");
    if (notGarbage) {
      if (isMML) callback(node);
      let childNode = node.firstChild;
      while (childNode) {
        this.traverseDOM(childNode, callback);
        childNode = childNode.nextSibling;
      }
    }
  }

  public init() {
    setGlobalMScene(this.mmlScene as IMMLScene);
    registerCustomElementsToWindow(window);
    this.clickTrigger = MMLClickTrigger.init(
      document,
      this.elementsHolder,
      this.mmlScene as IMMLScene,
    );
    this.promptManager = PromptManager.init(document.body);
    const { interactionListener } = InteractionManager.init(document.body, this.camera, this.scene);
    this.interactionListener = interactionListener;
  }
}
